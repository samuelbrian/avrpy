"""
leonardo.py
Port of the Arduino library, specifically the methods declared in 'Arduino.h'.

Samuel Brian
"""

from avr import *

# Defined in Arduino.h
HIGH = 0x1
LOW  = 0x0
INPUT        = 0x0
OUTPUT       = 0x1
INPUT_PULLUP = 0x2
LSBFIRST = 0
MSBFIRST = 1
CHANGE  = 1
FALLING = 2
RISING  = 3

class Arduino:

    def __init__(self, board):
        self.board = board
        self.avr = board.avr

        # Defined in Arduino.h
        if self.avr.defined("__AVR_ATtiny24__") or self.avr.defined("__AVR_ATtiny44__") or self.avr.defined("__AVR_ATtiny84__") or self.avr.defined("__AVR_ATtiny25__") or self.avr.defined("__AVR_ATtiny45__") or self.avr.defined("__AVR_ATtiny85__"):
            self.DEFAULT  = 0
            self.EXTERNAL = 1
            self.INTERNAL = 2
        else:
            if self.avr.defined("__AVR_ATmega1280__") or self.avr.defined("__AVR_ATmega2560__") or self.avr.defined("__AVR_ATmega1284__") or self.avr.defined("__AVR_ATmega1284P__") or self.avr.defined("__AVR_ATmega644__") or self.avr.defined("__AVR_ATmega644A__") or self.avr.defined("__AVR_ATmega644P__") or self.avr.defined("__AVR_ATmega644PA__"):
                self.INTERNAL1V1  = 2
                self.INTERNAL2V56 = 3
            else:
                self.INTERNAL     = 3
            self.DEFAULT  = 1
            self.EXTERNAL = 0

        self.analog_reference = self.DEFAULT

    def clockCyclesPerMicrosecond(self): return self.avr.F_CPU / 1000000
    def clockCyclesToMicroseconds(self, a): return a / self.clockCyclesPerMicrosecond()
    def microsecondsToClockCycles(self, a): return a * self.clockCyclesPerMicrosecond()

    def bitRead(self, value, bit): return ((value) >> (bit)) & 0x01
    #define bitSet(self, value, bit) ((value) |= (1UL << (bit)))
    #define bitClear(self, value, bit) ((value) &= ~(1UL << (bit)))
    #define bitWrite(self, value, bit, bitvalue) (bitvalue ? bitSet(value, bit) : bitClear(value, bit))

    def lowByte(w): return (w) & 0xff
    def highByte(w): return (w) >> 8

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
    def analogRead(self, pin):

        if "analogPinToChannel" in dir(self.board):
            if self.avr.defined("__AVR_ATmega32U4__"):
                if (pin >= 18): pin -= 18 # allow for channel or pin numbers
            pin = self.board.analogPinToChannel(pin)
        elif self.avr.defined("__AVR_ATmega1280__") or self.avr.defined("__AVR_ATmega2560__"):
            if (pin >= 54): pin -= 54 # allow for channel or pin numbers
        elif self.avr.defined("__AVR_ATmega32U4__"):
            if (pin >= 18): pin -= 18 # allow for channel or pin numbers
        elif self.avr.defined("__AVR_ATmega1284__") or self.avr.defined("__AVR_ATmega1284P__") or self.avr.defined("__AVR_ATmega644__") or self.avr.defined("__AVR_ATmega644A__") or self.avr.defined("__AVR_ATmega644P__") or self.avr.defined("__AVR_ATmega644PA__"):
            if (pin >= 24): pin -= 24 # allow for channel or pin numbers
        else:
            if (pin >= 14): pin -= 14 # allow for channel or pin numbers

        if self.avr.defined("ADCSRB") and self.avr.defined("MUX5"):
            # the MUX5 bit of ADCSRB selects whether we're reading from channels
            # 0 to 7 (MUX5 low) or 8 to 15 (MUX5 high).
            self.avr.ADCSRB = (self.avr.ADCSRB & invert(1 << self.avr.MUX5)) | (((pin >> 3) & 0x01) << self.avr.MUX5)

        if self.avr.defined("ADMUX"):
            # set the analog reference (high two bits of ADMUX) and select the
            # channel (low 4 bits).  this also sets ADLAR (left-adjust result)
            # to 0 (the default).
            self.avr.ADMUX = (self.analog_reference << 6) | (pin & 0x07)

        # without a delay, we seem to read from the wrong channel
        #delay(1);

        if self.avr.defined("ADCSRA") and self.avr.defined("ADCL"):
            # start the conversion
            self.avr.sbi("ADCSRA", self.avr.ADSC)

            # ADSC is cleared when the conversion finishes
            while (self.avr.bit_is_set("ADCSRA", self.avr.ADSC)): pass

            # we have to read ADCL first; doing so locks both ADCL
            # and ADCH until ADCH is read.  reading ADCL second would
            # cause the results of each conversion to be discarded,
            # as ADCL and ADCH would be locked when it completed.
            low  = self.avr.ADCL
            high = self.avr.ADCH
        else:
            # we dont have an ADC, return 0
            low  = 0
            high = 0

        # combine the two bytes
        return (high << 8) | low

    # Implemented in wiring_analog.c
    def analogReference(self, mode):
        self.analog_reference = mode

    # Implemented in wiring_analog.c
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

