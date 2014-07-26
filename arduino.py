"""
leonardo.py
Port of the Arduino library, specifically the methods declared in 'Arduino.h'.

Samuel Brian
"""

from avr import *
from time import sleep, time

# Defined in Arduino.h
HIGH = 0x1
LOW = 0x0
INPUT = 0x0
OUTPUT = 0x1
INPUT_PULLUP = 0x2
LSBFIRST = 0
MSBFIRST = 1
CHANGE = 1
FALLING = 2
RISING = 3


class Arduino:
    TIMER0A = 1
    TIMER0B = 2
    TIMER1A = 3
    TIMER1B = 4
    TIMER2 = 5
    TIMER2A = 6
    TIMER2B = 7

    TIMER3A = 8
    TIMER3B = 9
    TIMER3C = 10
    TIMER4A = 11
    TIMER4B = 12
    TIMER4C = 13
    TIMER4D = 14
    TIMER5A = 15
    TIMER5B = 16
    TIMER5C = 17

    PA = 1
    PB = 2
    PC = 3
    PD = 4
    PE = 5
    PF = 6
    PG = 7
    PH = 8
    PI = 9
    PJ = 10
    PK = 11
    PL = 12
    NOT_A_PORT = 0
    NOT_A_PIN = 0
    NOT_ON_TIMER = 0
    NOT_AN_INTERRUPT = -1

    def __init__(self, board):
        self.board = board
        self.avr = board.avr

        # Defined in Arduino.h
        if self.avr.defined("__AVR_ATtiny24__") or self.avr.defined("__AVR_ATtiny44__") or self.avr.defined(
                "__AVR_ATtiny84__") or self.avr.defined("__AVR_ATtiny25__") or self.avr.defined(
                "__AVR_ATtiny45__") or self.avr.defined("__AVR_ATtiny85__"):
            self.DEFAULT = 0
            self.EXTERNAL = 1
            self.INTERNAL = 2
        else:
            if self.avr.defined("__AVR_ATmega1280__") or self.avr.defined("__AVR_ATmega2560__") or self.avr.defined(
                    "__AVR_ATmega1284__") or self.avr.defined("__AVR_ATmega1284P__") or self.avr.defined(
                    "__AVR_ATmega644__") or self.avr.defined("__AVR_ATmega644A__") or self.avr.defined(
                    "__AVR_ATmega644P__") or self.avr.defined("__AVR_ATmega644PA__"):
                self.INTERNAL1V1 = 2
                self.INTERNAL2V56 = 3
            else:
                self.INTERNAL = 3
            self.DEFAULT = 1
            self.EXTERNAL = 0

        self.analog_reference = self.DEFAULT
        self.start_time_sec = time()  # seconds

    def clockCyclesPerMicrosecond(self):
        return self.avr.F_CPU / 1000000

    def clockCyclesToMicroseconds(self, a):
        return a / self.clockCyclesPerMicrosecond()

    def microsecondsToClockCycles(self, a):
        return a * self.clockCyclesPerMicrosecond()

    def bitRead(self, value, bit):
        return ((value) >> (bit)) & 0x01

    #define bitSet(self, value, bit) ((value) |= (1UL << (bit)))
    #define bitClear(self, value, bit) ((value) &= ~(1UL << (bit)))
    #define bitWrite(self, value, bit, bitvalue) (bitvalue ? bitSet(value, bit) : bitClear(value, bit))

    def lowByte(w):
        return (w) & 0xff

    def highByte(w):
        return (w) >> 8

    # void init(void);

    # Implementation from wiring_digital.c
    def pinMode(self, pin, mode):
        bit = self.digitalPinToBitMask(pin)
        port = self.digitalPinToPort(pin)

        if port == Arduino.NOT_A_PIN: return

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

    # Implementation from wiring_digital.c
    def digitalWrite(self, pin, val):
        timer = self.digitalPinToTimer(pin)
        bit = self.digitalPinToBitMask(pin)
        port = self.digitalPinToPort(pin)

        if port == Arduino.NOT_A_PIN: return

        # If the pin that support PWM output, we need to turn it off
        # before doing a digital write.
        if (timer != Arduino.NOT_ON_TIMER): self.turnOffPWM(timer)

        out = self.portOutputRegister(port)

        ##oldSREG = self.avr.SREG
        ##     cli();

        if val == LOW:
            out.set(out.get() & invert8(bit))  # *out &= ~bit
        else:
            out.set(out.get() | bit)  # *out |= bit

        ##self.avr.SREG = oldSREG

    # Implementation from wiring_digital.c
    def digitalRead(self, pin):
        timer = self.digitalPinToTimer(pin)
        bit = self.digitalPinToBitMask(pin)
        port = self.digitalPinToPort(pin)

        if port == Arduino.NOT_A_PIN: return LOW

        # If the pin that support PWM output, we need to turn it off
        # before getting a digital reading.
        if (timer != Arduino.NOT_ON_TIMER): self.turnOffPWM(timer)

        if self.portInputRegister(port).get() & bit: return HIGH
        return LOW

    # Implementation from wiring_digital.c
    def turnOffPWM(self, timer):
        if self.avr.defined("TCCR1A") and self.avr.defined("COM1A1"):
            if timer == Arduino.TIMER1A: self.avr.cbi("TCCR1A", self.avr.COM1A1)

        if self.avr.defined("TCCR1A") and self.avr.defined("COM1B1"):
            if timer == Arduino.TIMER1B: self.avr.cbi("TCCR1A", self.avr.COM1B1)

        if self.avr.defined("TCCR2") and self.avr.defined("COM21"):
            if timer == Arduino.TIMER2: self.avr.cbi("TCCR2", self.avr.COM21)

        if self.avr.defined("TCCR0A") and self.avr.defined("COM0A1"):
            if timer == Arduino.TIMER0A: self.avr.cbi("TCCR0A", self.avr.COM0A1)

        if self.avr.defined("TIMER0B") and self.avr.defined("COM0B1"):
            if timer == Arduino.TIMER0B: self.avr.cbi("TCCR0A", self.avr.COM0B1)

        if self.avr.defined("TCCR2A") and self.avr.defined("COM2A1"):
            if timer == Arduino.TIMER2A: self.avr.cbi("TCCR2A", self.avr.COM2A1)

        if self.avr.defined("TCCR2A") and self.avr.defined("COM2B1"):
            if timer == Arduino.TIMER2B: self.avr.cbi("TCCR2A", self.avr.COM2B1)

        if self.avr.defined("TCCR3A") and self.avr.defined("COM3A1"):
            if timer == Arduino.TIMER3A: self.avr.cbi("TCCR3A", self.avr.COM3A1)

        if self.avr.defined("TCCR3A") and self.avr.defined("COM3B1"):
            if timer == Arduino.TIMER3B: self.avr.cbi("TCCR3A", self.avr.COM3B1)

        if self.avr.defined("TCCR3A") and self.avr.defined("COM3C1"):
            if timer == Arduino.TIMER3C: self.avr.cbi("TCCR3A", self.avr.COM3C1)

        if self.avr.defined("TCCR4A") and self.avr.defined("COM4A1"):
            if timer == Arduino.TIMER4A: self.avr.cbi("TCCR4A", self.avr.COM4A1)

        if self.avr.defined("TCCR4A") and self.avr.defined("COM4B1"):
            if timer == Arduino.TIMER4B: self.avr.cbi("TCCR4A", self.avr.COM4B1)

        if self.avr.defined("TCCR4A") and self.avr.defined("COM4C1"):
            if timer == Arduino.TIMER4C: self.avr.cbi("TCCR4A", self.avr.COM4C1)

        if self.avr.defined("TCCR4C") and self.avr.defined("COM4D1"):
            if timer == Arduino.TIMER4D: self.avr.cbi("TCCR4C", self.avr.COM4D1)

        if self.avr.defined("TCCR5A"):
            if timer == Arduino.TIMER5A: self.avr.cbi("TCCR5A", self.avr.COM5A1)
            if timer == Arduino.TIMER5B: self.avr.cbi("TCCR5A", self.avr.COM5B1)
            if timer == Arduino.TIMER5C: self.avr.cbi("TCCR5A", self.avr.COM5C1)

    # Implementation from wiring_analog.c
    def analogRead(self, pin):

        if "analogPinToChannel" in dir(self.board):
            if self.avr.defined("__AVR_ATmega32U4__"):
                if (pin >= 18): pin -= 18  # allow for channel or pin numbers
            pin = self.board.analogPinToChannel(pin)
        elif self.avr.defined("__AVR_ATmega1280__") or self.avr.defined("__AVR_ATmega2560__"):
            if (pin >= 54): pin -= 54  # allow for channel or pin numbers
        elif self.avr.defined("__AVR_ATmega32U4__"):
            if (pin >= 18): pin -= 18  # allow for channel or pin numbers
        elif self.avr.defined("__AVR_ATmega1284__") or self.avr.defined("__AVR_ATmega1284P__") or self.avr.defined(
                "__AVR_ATmega644__") or self.avr.defined("__AVR_ATmega644A__") or self.avr.defined(
                "__AVR_ATmega644P__") or self.avr.defined("__AVR_ATmega644PA__"):
            if (pin >= 24): pin -= 24  # allow for channel or pin numbers
        else:
            if (pin >= 14): pin -= 14  # allow for channel or pin numbers

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
            low = self.avr.ADCL
            high = self.avr.ADCH
        else:
            # we dont have an ADC, return 0
            low = 0
            high = 0

        # combine the two bytes
        return (high << 8) | low

    # Implementation from wiring_analog.c
    def analogReference(self, mode):
        self.analog_reference = mode

    # Implementation from wiring_analog.c
    # void analogWrite(uint8_t, int);
    def analogWrite(self, pin, val):

        # We need to make sure the PWM output is enabled for those pins
        # that support it, as we turn it off when digitally reading or
        # writing with them.  Also, make sure the pin is in output mode
        # for consistenty with Wiring, which doesn't require a pinMode
        # call for the analog output pins.
        self.pinMode(pin, OUTPUT)
        if (val == 0):
            self.digitalWrite(pin, LOW)
        elif (val == 255):
            self.digitalWrite(pin, HIGH)
        else:
            timer = self.digitalPinToTimer(pin)

            if timer == "NOT_ON_TIMER":  # Moved this up from bottom [samuelbr]
                if (val < 128):
                    self.digitalWrite(pin, LOW)
                else:
                    self.digitalWrite(pin, HIGH)
                return

            # XXX fix needed for atmega8
            if self.avr.defined("TCCR0") and self.avr.defined("COM00") and not self.avr.defined("__AVR_ATmega8__"):
                if timer == Arduino.TIMER0A:
                    # connect pwm to pin on timer 0
                    self.avr.sbi("TCCR0", self.avr.COM00)
                    self.avr.OCR0 = val  # set pwm duty
                    return

            if self.avr.defined("TCCR0A") and self.avr.defined("COM0A1"):
                if timer == Arduino.TIMER0A:
                    # connect pwm to pin on timer 0, channel A
                    self.avr.sbi("TCCR0A", self.avr.COM0A1)
                    self.avr.OCR0A = val  # set pwm duty
                    return

            if self.avr.defined("TCCR0A") and self.avr.defined("COM0B1"):
                if timer == Arduino.TIMER0B:
                    # connect pwm to pin on timer 0, channel B
                    self.avr.sbi("TCCR0A", self.avr.COM0B1)
                    self.avr.OCR0B = val  # set pwm duty
                    return

            if self.avr.defined("TCCR1A") and self.avr.defined("COM1A1"):
                if timer == Arduino.TIMER1A:
                    # connect pwm to pin on timer 1, channel A
                    self.avr.sbi("TCCR1A", self.avr.COM1A1)
                    self.avr.OCR1A = val  # set pwm duty
                    return

            if self.avr.defined("TCCR1A") and self.avr.defined("COM1B1"):
                if timer == Arduino.TIMER1B:
                    # connect pwm to pin on timer 1, channel B
                    self.avr.sbi("TCCR1A", self.avr.COM1B1)
                    self.avr.OCR1B = val  # set pwm duty
                    return

            if self.avr.defined("TCCR2") and self.avr.defined("COM21"):
                if timer == Arduino.TIMER2:
                    # connect pwm to pin on timer 2
                    self.avr.sbi("TCCR2", self.avr.COM21)
                    self.avr.OCR2 = val  # set pwm duty
                    return

            if self.avr.defined("TCCR2A") and self.avr.defined("COM2A1"):
                if timer == Arduino.TIMER2A:
                    # connect pwm to pin on timer 2, channel A
                    self.avr.sbi("TCCR2A", self.avr.COM2A1)
                    self.avr.OCR2A = val  # set pwm duty
                    return

            if self.avr.defined("TCCR2A") and self.avr.defined("COM2B1"):
                if timer == Arduino.TIMER2B:
                    # connect pwm to pin on timer 2, channel B
                    self.avr.sbi("TCCR2A", self.avr.COM2B1)
                    self.avr.OCR2B = val  # set pwm duty
                    return

            if self.avr.defined("TCCR3A") and self.avr.defined("COM3A1"):
                if timer == Arduino.TIMER3A:
                    # connect pwm to pin on timer 3, channel A
                    self.avr.sbi("TCCR3A", self.avr.COM3A1)
                    self.avr.OCR3A = val  # set pwm duty
                    return

            if self.avr.defined("TCCR3A") and self.avr.defined("COM3B1"):
                if timer == Arduino.TIMER3B:
                    # connect pwm to pin on timer 3, channel B
                    self.avr.sbi("TCCR3A", self.avr.COM3B1)
                    self.avr.OCR3B = val  # set pwm duty
                    return

            if self.avr.defined("TCCR3A") and self.avr.defined("COM3C1"):
                if timer == Arduino.TIMER3C:
                    # connect pwm to pin on timer 3, channel C
                    self.avr.sbi("TCCR3A", self.avr.COM3C1)
                    self.avr.OCR3C = val  # set pwm duty
                    return

            if self.avr.defined("TCCR4A"):
                if timer == Arduino.TIMER4A:
                    #connect pwm to pin on timer 4, channel A
                    self.avr.sbi("TCCR4A", self.avr.COM4A1)
                    if self.avr.defined("COM4A0"):  # only used on 32U4
                        self.avr.cbi("TCCR4A", self.avr.COM4A0)
                    self.avr.OCR4A = val  # set pwm duty
                    return

            if self.avr.defined("TCCR4A") and self.avr.defined("COM4B1"):
                if timer == Arduino.TIMER4B:
                    # connect pwm to pin on timer 4, channel B
                    self.avr.sbi("TCCR4A", self.avr.COM4B1)
                    self.avr.OCR4B = val  # set pwm duty
                    return

            if self.avr.defined("TCCR4A") and self.avr.defined("COM4C1"):
                if timer == Arduino.TIMER4C:
                    # connect pwm to pin on timer 4, channel C
                    self.avr.sbi("TCCR4A", self.avr.COM4C1)
                    self.avr.OCR4C = val  # set pwm duty
                    return

            if self.avr.defined("TCCR4C") and self.avr.defined("COM4D1"):
                if timer == Arduino.TIMER4D:
                    # connect pwm to pin on timer 4, channel D
                    self.avr.sbi("TCCR4C", self.avr.COM4D1)
                    if self.avr.defined("COM4D0"):  # only used on 32U4
                        self.avr.cbi("TCCR4C", self.avr.COM4D0)
                    self.avr.OCR4D = val  # set pwm duty
                    return

            if self.avr.defined("TCCR5A") and self.avr.defined("COM5A1"):
                if timer == Arduino.TIMER5A:
                    # connect pwm to pin on timer 5, channel A
                    self.avr.sbi("TCCR5A", self.avr.COM5A1)
                    self.avr.OCR5A = val  # set pwm duty
                    return

            if self.avr.defined("TCCR5A") and self.avr.defined("COM5B1"):
                if timer == Arduino.TIMER5B:
                    # connect pwm to pin on timer 5, channel B
                    self.avr.sbi("TCCR5A", self.avr.COM5B1)
                    self.avr.OCR5B = val  # set pwm duty
                    return

            if self.avr.defined("TCCR5A") and self.avr.defined("COM5C1"):
                if timer == Arduino.TIMER5C:
                    # connect pwm to pin on timer 5, channel C
                    self.avr.sbi("TCCR5A", self.avr.COM5C1)
                    self.avr.OCR5C = val  # set pwm duty
                    return

    # The Arduino time functions (implemented in wiring.c) rely on local variables updated in the TIMER0_OVF ISR and
    # can't be accessed through the SFR bridge. Plus, the overhead with the serial communication would make timing
    # very difficult. So here are Python implementations of the time functions:
    def millis(self):
        return (time() - self.start_time_sec)*1000.0

    def micros(self):
        return (time() - self.start_time_sec)*1000000.0

    def delay(self, ms):
        sleep(ms/1000.0)

    def delayMicroseconds(self, us):
        sleep(us/1000000.0)

    # unsigned long pulseIn(uint8_t pin, uint8_t state, unsigned long timeout);

    # Implementation from wiring_shift.c
    def shiftOut(self, dataPin, clockPin, bitOrder, val):
        for i in range(0, 8):
            if (bitOrder == LSBFIRST):
                self.digitalWrite(dataPin, not not (val & (1 << i)))
            else:
                self.digitalWrite(dataPin, not not (val & (1 << (7 - i))))

            self.digitalWrite(clockPin, HIGH)
            self.digitalWrite(clockPin, LOW)

    # Implementation from wiring_shift.c
    def shiftIn(self, dataPin, clockPin, bitOrder):
        value = 0
        for i in range(0, 8):
            self.digitalWrite(clockPin, HIGH)
            if (bitOrder == LSBFIRST):
                value |= self.digitalRead(dataPin) << i
            else:
                value |= self.digitalRead(dataPin) << (7 - i)
            self.digitalWrite(clockPin, LOW)
        return value

    # Implementation from WInterrupts.c
    # void attachInterrupt(uint8_t, void (*)(void), int mode);
    # void detachInterrupt(uint8_t);

    def digitalPinToPort(self, P):
        return self.board.digital_pin_to_port_PGM[P]

    def digitalPinToBitMask(self, P):
        return self.board.digital_pin_to_bit_mask_PGM[P]

    def digitalPinToTimer(self, P):
        return self.board.digital_pin_to_timer_PGM[P]

    def analogInPinToBit(self, P):
        return P

    def portOutputRegister(self, P):
        return self.board.port_to_output_PGM[P]

    def portInputRegister(self, P):
        return self.board.port_to_input_PGM[P]

    def portModeRegister(self, P):
        return self.board.port_to_mode_PGM[P]

