/*
** Piper layer. 
** 
** Author: Samuel Brian
*/

#ifndef ROBOT_PIPER_H
#define ROBOT_PIPER_H

#include <Arduino.h>

#define PACKET_BEGIN 		0xBE
#define PACKET_END 			0xEF
#define MAX_PIPE_ID 		0xFF
#define MAX_DATA_LENGTH		0xFF

#define MAX_READ_CALLBACKS	2

/******************************************************************************
** Piper - pseudo-asynchronous only.
******************************************************************************/

class Piper {	
	public:
		
		Piper(Stream& stream);
		
		Piper() {};
		
		/* Write a complete packet to the stream. */
		void writePacket(uint8_t pipeId, uint8_t *data, uint8_t dataLength);
		
		/* Send the PACKET_BEGIN token and the destination pipe. */
		void writeBegin(uint8_t pipeId);
		
		/* Write a byte to the write-buffer. */
		uint8_t write(uint8_t data);
		
		/* Write a number of bytes to the write-buffer. */
		uint8_t write(uint8_t *data, uint8_t dataLength);
		
		/* Send the write-buffer's length and contents, and the PACKET_END token. */
		void writeEnd();

		typedef void (*ReadCallback)(Stream&);
		
		/* Set the packet callback function for a pipe. */
		void setReadCallback(uint8_t pipeId, ReadCallback callback);
		
		/* Read one packet from the stream and call the associated callback function. */
		void readPacketFromStream();
		
		/* Loop reading packets from the stream. */
		void start();
		
		/* Stops the start() function after it processes the current packet. */
		void stop();

		friend class PacketStream;
		
	private:
		
		// Source stream
		Stream *streamp;
		
		uint8_t writeBuffer[MAX_DATA_LENGTH];
		uint8_t writeLength;
		
		uint8_t readBuffer[MAX_DATA_LENGTH];
		uint8_t readLength;
		ReadCallback callbacks[MAX_READ_CALLBACKS];
		
		void readBytes(uint8_t *buffer, uint8_t length);
		uint8_t readByte();
		volatile bool stopped;
};

/******************************************************************************
** PacketStream - provides a Stream interface to Piper packets
******************************************************************************/

class PacketStream : public Stream {
	public:
	
		PacketStream(Piper& piper, uint8_t pipeId);
		
		/* Write a byte to the packet write-buffer */
		virtual size_t write(uint8_t data);
		
		virtual int available();
		
		/* Read the next byte from the packet read-buffer. */
		virtual int read();
		
		virtual int peek();
		
		/* Sends a response packet if any data has been written. */
		virtual void flush();
		
	private:		
		Piper *piper;
		
		/* Pipe number that written data is sent to. */
		uint8_t pipeId;
		
		/* Read location of this PacketStream into the packet's read-buffer. */
		uint8_t readIndex;
};

#endif
