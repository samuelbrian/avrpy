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

#define NUM_VECTORS     43
uint8_t interruptEnabled[NUM_VECTORS];

#define MAX_INTERRUPT_QUEUE 10
volatile uint8_t triggeredInterruptsQueue[MAX_INTERRUPT_QUEUE];
volatile uint8_t triggeredInterruptsIndex;

Piper piper;

void registerPipeRead(Stream& packet);
void interruptPipeRead(Stream& packet);
void triggerInterrupt(uint8_t vectorNumber);

void setup() {
    for (uint8_t i = 0; i < NUM_VECTORS; i++) {
        interruptEnabled[i] = INT_DISABLE;
    }
    Serial.begin(38400);
    piper = Piper(Serial);
    triggeredInterruptsIndex = 0;
    piper.setReadCallback(REGISTER_PIPE, registerPipeRead);
    piper.setReadCallback(INTERRUPT_PIPE, interruptPipeRead);
}

void loop() {
    //piper.start();
    cli();
    if (triggeredInterruptsIndex > 0) {
        uint8_t vectorNumber = triggeredInterruptsQueue[--triggeredInterruptsIndex];
        //sei();
        piper.writePacket(INTERRUPT_PIPE, &vectorNumber, 1);
        //piper.writePacket(INTERRUPT_PIPE, (uint8_t*)&triggeredInterruptsIndex, 1);
    }
    sei();
    if (Serial.available()) piper.readPacketFromStream();
}

void triggerInterrupt(uint8_t vectorNumber) {
    if (interruptEnabled[vectorNumber] == INT_ENABLE && triggeredInterruptsIndex < MAX_INTERRUPT_QUEUE) {
        //digitalWrite(13, !digitalRead(13));
        triggeredInterruptsQueue[triggeredInterruptsIndex++] = vectorNumber;
    }
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
      
    } else if (token == WRITE_IO8) {
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
    
}

void interruptPipeRead(Stream& packet) {
    interruptEnabled[packet.read()] = packet.read();
}

ISR(INT0_vect) { triggerInterrupt(1); }
ISR(INT1_vect) { triggerInterrupt(2); }
ISR(INT2_vect) { triggerInterrupt(3); }
ISR(INT3_vect) { triggerInterrupt(4); }
ISR(INT6_vect) { triggerInterrupt(7); }
ISR(PCINT0_vect) { triggerInterrupt(9); }
//ISR(USB_GEN_vect) { triggerInterrupt(10); } // Used by Arduino
//ISR(USB_COM_vect) { triggerInterrupt(11); } // Used by Arduino
ISR(WDT_vect) { triggerInterrupt(12); }
ISR(TIMER1_CAPT_vect) { triggerInterrupt(16); }
ISR(TIMER1_COMPA_vect) { triggerInterrupt(17); }
ISR(TIMER1_COMPB_vect) { triggerInterrupt(18); }
ISR(TIMER1_COMPC_vect) { triggerInterrupt(19); }
ISR(TIMER1_OVF_vect) { triggerInterrupt(20); }
ISR(TIMER0_COMPA_vect) { triggerInterrupt(21); }
ISR(TIMER0_COMPB_vect) { triggerInterrupt(22); }
//ISR(TIMER0_OVF_vect) { triggerInterrupt(23); } // Used by Arduino
ISR(SPI_STC_vect) { triggerInterrupt(24); }
ISR(USART1_RX_vect) { triggerInterrupt(25); }
ISR(USART1_UDRE_vect) { triggerInterrupt(26); }
ISR(USART1_TX_vect) { triggerInterrupt(27); }
ISR(ANALOG_COMP_vect) { triggerInterrupt(28); }
ISR(ADC_vect) { triggerInterrupt(29); }
ISR(EE_READY_vect) { triggerInterrupt(30); }
ISR(TIMER3_CAPT_vect) { triggerInterrupt(31); }
ISR(TIMER3_COMPA_vect) { triggerInterrupt(32); }
ISR(TIMER3_COMPB_vect) { triggerInterrupt(33); }
ISR(TIMER3_COMPC_vect) { triggerInterrupt(34); }
ISR(TIMER3_OVF_vect) { triggerInterrupt(35); }
ISR(TWI_vect) { triggerInterrupt(36); }
ISR(SPM_READY_vect) { triggerInterrupt(37); }
ISR(TIMER4_COMPA_vect) { triggerInterrupt(38); }
ISR(TIMER4_COMPB_vect) { triggerInterrupt(39); }
ISR(TIMER4_COMPD_vect) { triggerInterrupt(40); }
ISR(TIMER4_OVF_vect) { triggerInterrupt(41); }
ISR(TIMER4_FPF_vect) { triggerInterrupt(42); }


