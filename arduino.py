"""
leonardo.py
Port of the Arduino library, specifically the methods declared in 'Arduino.h'.

Samuel Brian
"""

from avr import *

HIGH = 0x1
LOW  = 0x0

INPUT        = 0x0
OUTPUT       = 0x1
INPUT_PULLUP = 0x2

PI         = 3.1415926535897932384626433832795
HALF_PI    = 1.5707963267948966192313216916398
TWO_PI     = 6.283185307179586476925286766559
DEG_TO_RAD = 0.017453292519943295769236907684886
RAD_TO_DEG = 57.295779513082320876798154814105
EULER      = 2.718281828459045235360287471352

LSBFIRST = 0
MSBFIRST = 1

CHANGE  = 1
FALLING = 2
RISING  = 3

class Arduino:

    def __init__(self, board):
        self.board = board
        self.avr = board.avr

    def clockCyclesPerMicrosecond(self): return self.avr.F_CPU / 1000000
    def clockCyclesToMicroseconds(self, a): return a / self.clockCyclesPerMicrosecond()
    def microsecondsToClockCycles(self, a): return a * self.clockCyclesPerMicrosecond()

    def bitRead(self, value, bit): return ((value) >> (bit)) & 0x01
    #define bitSet(self, value, bit) ((value) |= (1UL << (bit)))
    #define bitClear(self, value, bit) ((value) &= ~(1UL << (bit)))
    #define bitWrite(self, value, bit, bitvalue) (bitvalue ? bitSet(value, bit) : bitClear(value, bit))

    def lowByte(w): return (w) & 0xff
    def highByte(w): return ((w) >> 8)

    # void init(void);

    # Implemented in wiring_digital.c
    def pinMode(self, pin, mode):
        bit = self.digitalPinToBitMask(pin)
        port = self.digitalPinToPort(pin)

        if port == self.board.NOT_A_PIN: return

        reg = self.portModeRegister(port)
        out = self.portOutputRegister(port)

        if mode == INPUT:
            ##oldSREG = self.avr.SREG
            ##     cli();
            reg.set(reg.get() & invert8(bit))  # *reg &= ~bit;
            out.set(out.get() & invert8(bit))  # *out &= ~bit
            ##self.avr.SREG = oldSREG
        elif mode == INPUT_PULLUP:
            ##oldSREG = self.avr.SREG
            ##    cli();
            reg.set(reg.get() & invert8(bit))  # *reg &= ~bit;
            out.set(out.get() | bit)  # *out |= bit
            ##self.avr.SREG = oldSREG
        else:
            ##oldSREG = self.avr.SREG
            ##     cli();
            reg.set(reg.get() | bit)  # *reg |= bit;
            ##self.avr.SREG = oldSREG

    # Implemented in wiring_digital.c
    def digitalWrite(self, pin, val):
        timer = self.digitalPinToTimer(pin)
        bit = self.digitalPinToBitMask(pin)
        port = self.digitalPinToPort(pin)

        if port == self.board.NOT_A_PIN: return

        # If the pin that support PWM output, we need to turn it off
        # before doing a digital write.
        ##if (timer != NOT_ON_TIMER) turnOffPWM(timer);

        out = self.portOutputRegister(port)

        ##oldSREG = self.avr.SREG
        ##     cli();

        if val == LOW:
            out.set(out.get() & invert8(bit))  # *out &= ~bit
        else:
            out.set(out.get() | bit)  # *out |= bit

        ##self.avr.SREG = oldSREG

    # Implemented in wiring_digital.c
    def digitalRead(self, pin):
        timer = self.digitalPinToTimer(pin)
        bit = self.digitalPinToBitMask(pin)
        port = self.digitalPinToPort(pin)

        if port == self.board.NOT_A_PIN: return LOW

        # If the pin that support PWM output, we need to turn it off
        # before getting a digital reading.
        #if (timer != NOT_ON_TIMER) turnOffPWM(timer);

        if self.portInputRegister(port).get() & bit: return HIGH
        return LOW

    # Implemented in wiring_analog.c
    # int analogRead(uint8_t);
    # void analogReference(uint8_t mode);
    # void analogWrite(uint8_t, int);

    # unsigned long millis(void);
    # unsigned long micros(void);
    # void delay(unsigned long);
    # void delayMicroseconds(unsigned int us);
    # unsigned long pulseIn(uint8_t pin, uint8_t state, unsigned long timeout);
    #
    # void shiftOut(uint8_t dataPin, uint8_t clockPin, uint8_t bitOrder, uint8_t val);
    # uint8_t shiftIn(uint8_t dataPin, uint8_t clockPin, uint8_t bitOrder);

    # Implemented in WInterrupts.c
    # void attachInterrupt(uint8_t, void (*)(void), int mode);
    # void detachInterrupt(uint8_t);





    def digitalPinToPort(self, P):      return self.board.digital_pin_to_port_PGM[P]
    def digitalPinToBitMask(self, P):   return self.board.digital_pin_to_bit_mask_PGM[P]
    def digitalPinToTimer(self, P):     return self.board.digital_pin_to_timer_PGM[P]
    def analogInPinToBit(self, P):      return P
    def portOutputRegister(self, P):    return self.board.port_to_output_PGM[P]
    def portInputRegister(self, P):     return self.board.port_to_input_PGM[P]
    def portModeRegister(self, P):      return self.board.port_to_mode_PGM[P]

