/*
** Author: Samuel Brian
*/

#include "piper.h"

/******************************************************************************
** Piper
******************************************************************************/

Piper::Piper(Stream& stream) {
	streamp = &stream;
	writeLength = 0;
	
	for (uint8_t i = 0; i < MAX_READ_CALLBACKS; i++) {
		callbacks[i] = NULL;
	}
}

void Piper::writePacket(uint8_t pipeId, uint8_t *data, uint8_t dataLength) {
	streamp->write(PACKET_BEGIN);
	streamp->write(pipeId);
	streamp->write(dataLength);
	streamp->write(data, dataLength);
	streamp->write(PACKET_END);
}

void Piper::writeBegin(uint8_t pipeId) {
	streamp->write(PACKET_BEGIN);
	streamp->write(pipeId);
}

uint8_t Piper::write(uint8_t data) {

	if (writeLength == MAX_DATA_LENGTH) {
		return 0;
	}	
	writeBuffer[writeLength++] = data;
	return 1;
}

uint8_t Piper::write(uint8_t *data, uint8_t dataLength) {
	
	uint8_t numBytes = 0;
	for (uint8_t i = 0; i < dataLength; i++) {
		if (write(data[i]) == 1) {			
			numBytes++;
		} else {
			break;
		}
	}
	
	return numBytes;
}

void Piper::writeEnd() {
	streamp->write(writeLength);
	streamp->write(writeBuffer, writeLength);
	streamp->write(PACKET_END);
	writeLength = 0;
}

void Piper::setReadCallback(uint8_t pipeId, ReadCallback callback) {	
	if (pipeId < MAX_READ_CALLBACKS) {
		callbacks[pipeId] = callback;
	}	
}

void Piper::readPacketFromStream() {
	uint8_t pipeId, endByte = 0x00;
	
	while (endByte != PACKET_END) {
		while (readByte() != PACKET_BEGIN) ;	
		pipeId = readByte();	
		readLength = readByte();
		readBytes(readBuffer, readLength);	
		endByte = readByte();
	}
	
	if (pipeId < MAX_READ_CALLBACKS && callbacks[pipeId] != NULL) {
		PacketStream ps(*this, pipeId);
		callbacks[pipeId](ps);
		ps.flush();
	}
	
}

void Piper::start() {
	stopped = false;
	while (!stopped) {
		readPacketFromStream();
	}
}

void Piper::stop() {
	stopped = true;
}

void Piper::readBytes(uint8_t *readBuffer, uint8_t length) {	
	uint8_t bytesRead = 0;
	while (bytesRead < length) {
		readBuffer[bytesRead++] = readByte();
	}		
}

uint8_t Piper::readByte() {
	int res = -1;
	while (res < 0) {
		// Keep reading until valid data arrives
		res = streamp->read();
	}
	return (uint8_t)res;
}

/******************************************************************************
** PacketStream
******************************************************************************/

PacketStream::PacketStream(Piper& piper, uint8_t pipeId) {
	piper.writeLength = 0;
	this->piper = &piper;
	readIndex = 0;
	this->pipeId = pipeId;
}

size_t PacketStream::write(uint8_t data) {
	return piper->write(data);
}

int PacketStream::available() {
	return readIndex < piper->readLength;
}

int PacketStream::read() {
	if (!available()) {
		return -1;
	}
	return piper->readBuffer[readIndex++];
}

int PacketStream::peek() {
	if (!available()) {
		return -1;
	}
	return piper->readBuffer[readIndex];
}

void PacketStream::flush() {
	if (piper->writeLength > 0) {
		piper->writeBegin(pipeId);
		piper->writeEnd();
	}
}
