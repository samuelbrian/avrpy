#include "piper.h"

// Pipe addresses
#define REGISTER_PIPE   0x00
#define INTERRUPT_PIPE  0x01

// Operation tokens
#define READ_IO8        0x01
#define READ_IO16       0x02
#define READ_MEM8       0x03
#define READ_MEM16      0x04
#define WRITE_IO8       0xF1
#define WRITE_IO16      0xF2
#define WRITE_MEM8      0xF3
#define WRITE_MEM16     0xF4

#define INT_ENABLE      0x01
#define INT_DISABLE     0x00

Piper piper;

void registerPipeRead(Stream& packet);
void interruptPipeRead(Stream& packet);

void setup() {
  Serial.begin(38400);
  piper = Piper(Serial);
  piper.setReadCallback(REGISTER_PIPE, registerPipeRead);
  piper.setReadCallback(INTERRUPT_PIPE, interruptPipeRead);
}

void loop() {
  piper.start();
}

void registerPipeRead(Stream& packet) {
    uint8_t *ptr = (uint8_t*)packet.read();
    uint8_t token = packet.read();
    
    if (token == READ_IO8) {
      packet.write(_SFR_IO8(ptr));
    } else if(token == READ_IO16) {
      packet.write(_SFR_IO8(ptr++));
      packet.write(_SFR_IO8(ptr));
    } else if (token == READ_MEM8) {
      packet.write(_SFR_MEM8(ptr));
    } else if(token == READ_MEM16) {
      packet.write(_SFR_MEM8(ptr++));
      packet.write(_SFR_MEM8(ptr));
    }
    
    if (token == WRITE_IO8) {
      _SFR_IO8(ptr) = packet.read();
    } else if(token == WRITE_IO16) {
      _SFR_IO8(ptr++) = packet.read();
      _SFR_IO8(ptr) = packet.read();
    } else if (token == WRITE_MEM8) {
      _SFR_MEM8(ptr) = packet.read();
    } else if(token == WRITE_MEM16) {
      _SFR_MEM8(ptr++) = packet.read();
      _SFR_MEM8(ptr) = packet.read();
    }
    
    /*
    } else if (token == WRITE8) {
      *ptr = (uint8_t)packet.read();
    } else if (token == WRITE16) {
      *ptr = (uint8_t)packet.read();
      ptr++;
      *ptr = (uint8_t)packet.read();
    }*/
    
}

void interruptPipeRead(Stream& packet) {
  
}
