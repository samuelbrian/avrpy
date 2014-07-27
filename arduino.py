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

    # Defined in Arduino.h
    # TODO: use avr.define() to put them with all the other defines
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

        # Defined in wiring_private.h
        if self.avr.defined("__AVR_ATmega1280__") or self.avr.defined("__AVR_ATmega2560__"):
            self.EXTERNAL_NUM_INTERRUPTS = 8
        if self.avr.defined("__AVR_ATmega1284__") or self.avr.defined("__AVR_ATmega1284P__") or self.avr.defined("__AVR_ATmega644__") or self.avr.defined("__AVR_ATmega644A__") or self.avr.defined("__AVR_ATmega644P__") or self.avr.defined("__AVR_ATmega644PA__"):
            self.EXTERNAL_NUM_INTERRUPTS = 3
        elif self.avr.defined("__AVR_ATmega32U4__"):
            self.EXTERNAL_NUM_INTERRUPTS = 5
        else:
            self.EXTERNAL_NUM_INTERRUPTS = 2

        self.analog_reference = self.DEFAULT
        self.start_time_sec = time()  # seconds

        self.init()

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

    # Implementation from wiring.c
    def init(self):

            # on the ATmega168, timer 0 is also used for fast hardware pwm
            # (using phase-correct PWM would mean that timer 0 overflowed half as often
            # resulting in different millis() behavior on the ATmega8 and ATmega168)
        if self.avr.defined("TCCR0A") and self.avr.defined("WGM01"):
            self.avr.sbi("TCCR0A", self.avr.WGM01)
            self.avr.sbi("TCCR0A", self.avr.WGM00)

            # set timer 0 prescale factor to 64
        if self.avr.defined("__AVR_ATmega128__"):
            # CPU specific: different values for the ATmega128
            self.avr.sbi("TCCR0", self.avr.CS02)
        elif self.avr.defined("TCCR0") and self.avr.defined("CS01") and self.avr.defined("CS00"):
            # this combination is for the standard atmega8
            self.avr.sbi("TCCR0", self.avr.CS01)
            self.avr.sbi("TCCR0", self.avr.CS00)
        elif self.avr.defined("TCCR0B") and self.avr.defined("CS01") and self.avr.defined("CS00"):
            # this combination is for the standard 168/328/1280/2560
            self.avr.sbi("TCCR0B", self.avr.CS01)
            self.avr.sbi("TCCR0B", self.avr.CS00)
        elif self.avr.defined("TCCR0A") and self.avr.defined("CS01") and self.avr.defined("CS00"):
            # this combination is for the __AVR_ATmega645__ series
            self.avr.sbi("TCCR0A", self.avr.CS01)
            self.avr.sbi("TCCR0A", self.avr.CS00)
        else:
            raise Exception("error Timer 0 prescale factor 64 not set correctly")
        
    
            # enable timer 0 overflow interrupt
        if self.avr.defined("TIMSK") and self.avr.defined("TOIE0"):
            self.avr.sbi("TIMSK", self.avr.TOIE0)
        elif self.avr.defined("TIMSK0") and self.avr.defined("TOIE0"):
            self.avr.sbi("TIMSK0", self.avr.TOIE0)
        else:
            raise Exception("error	Timer 0 overflow interrupt not set correctly")
        
    
            # timers 1 and 2 are used for phase-correct hardware pwm
            # this is better for motors as it ensures an even waveform
            # note, however, that fast pwm mode can achieve a frequency of up
            # 8 MHz (with a 16 MHz clock) at 50% duty cycle
    
        if self.avr.defined("TCCR1B") and self.avr.defined("CS11") and self.avr.defined("CS10"):
            self.avr.TCCR1B = 0
    
            # set timer 1 prescale factor to 64
            self.avr.sbi("TCCR1B", self.avr.CS11)
            if self.avr.F_CPU >= 8000000:
                self.avr.sbi("TCCR1B", self.avr.CS10)
        
        elif self.avr.defined("TCCR1") and self.avr.defined("CS11") and self.avr.defined("CS10"):
            self.avr.sbi("TCCR1", self.avr.CS11)
            if self.avr.F_CPU >= 8000000:
                self.avr.sbi("TCCR1", self.avr.CS10)
        
        
            # put timer 1 in 8-bit phase correct pwm mode
        if self.avr.defined("TCCR1A") and self.avr.defined("WGM10"):
            self.avr.sbi("TCCR1A", self.avr.WGM10)
        elif self.avr.defined("TCCR1"):
            raise Warning("warning this needs to be finished")
        
    
            # set timer 2 prescale factor to 64
        if self.avr.defined("TCCR2") and self.avr.defined("CS22"):
            self.avr.sbi("TCCR2", self.avr.CS22)
        elif self.avr.defined("TCCR2B") and self.avr.defined("CS22"):
            self.avr.sbi("TCCR2B", self.avr.CS22)
        else:
            raise Warning("warning Timer 2 not finished (may not be present on this CPU)")
        

            # configure timer 2 for phase correct pwm (8-bit)
        if self.avr.defined("TCCR2") and self.avr.defined("WGM20"):
            self.avr.sbi("TCCR2", self.avr.WGM20)
        elif self.avr.defined("TCCR2A") and self.avr.defined("WGM20"):
            self.avr.sbi("TCCR2A", self.avr.WGM20)
        else:
            raise Warning("warning Timer 2 not finished (may not be present on this CPU)")
        
    
        if self.avr.defined("TCCR3B") and self.avr.defined("CS31") and self.avr.defined("WGM30"):
            self.avr.sbi("TCCR3B", self.avr.CS31)		# set timer 3 prescale factor to 64
            self.avr.sbi("TCCR3B", self.avr.CS30)
            self.avr.sbi("TCCR3A", self.avr.WGM30)		# put timer 3 in 8-bit phase correct pwm mode
        
    
        if self.avr.defined("TCCR4A") and self.avr.defined("TCCR4B") and self.avr.defined("TCCR4D"): ## beginning of timer4 block for 32U4 and similar ##
            self.avr.sbi("TCCR4B", self.avr.CS42)		# set timer4 prescale factor to 64
            self.avr.sbi("TCCR4B", self.avr.CS41)
            self.avr.sbi("TCCR4B", self.avr.CS40)
            self.avr.sbi("TCCR4D", self.avr.WGM40)		# put timer 4 in phase- and frequency-correct PWM mode
            self.avr.sbi("TCCR4A", self.avr.PWM4A)		# enable PWM mode for comparator OCR4A
            self.avr.sbi("TCCR4C", self.avr.PWM4D)		# enable PWM mode for comparator OCR4D
        else: ## beginning of timer4 block for ATMEGA1280 and ATMEGA2560 ##
            if self.avr.defined("TCCR4B") and self.avr.defined("CS41") and self.avr.defined("WGM40"):
                self.avr.sbi("TCCR4B", self.avr.CS41)		# set timer 4 prescale factor to 64
                self.avr.sbi("TCCR4B", self.avr.CS40)
                self.avr.sbi("TCCR4A", self.avr.WGM40)		# put timer 4 in 8-bit phase correct pwm mode

            ## end timer4 block for ATMEGA1280/2560 and similar ##
    
        if self.avr.defined("TCCR5B") and self.avr.defined("CS51") and self.avr.defined("WGM50"):
            self.avr.sbi("TCCR5B", self.avr.CS51)		# set timer 5 prescale factor to 64
            self.avr.sbi("TCCR5B", self.avr.CS50)
            self.avr.sbi("TCCR5A", self.avr.WGM50)		# put timer 5 in 8-bit phase correct pwm mode
        
    
        if self.avr.defined("ADCSRA"):
            # set a2d prescale factor to 128
            # 16 MHz / 128 = 125 KHz, inside the desired 50-200 KHz range.
            # XXX: this will not work properly for other clock speeds, and
            # this code should use F_CPU to determine the prescale factor.
            self.avr.sbi("ADCSRA", self.avr.ADPS2)
            self.avr.sbi("ADCSRA", self.avr.ADPS1)
            self.avr.sbi("ADCSRA", self.avr.ADPS0)
    
            # enable a2d conversions
            self.avr.sbi("ADCSRA", self.avr.ADEN)
        
    
        #     # the bootloader connects pins 0 and 1 to the USART disconnect them
        #     # here so they can be used as normal digital i/o they will be
        #     # reconnected in Serial.begin()
        # if self.avr.defined("UCSRB"):
        #     UCSRB = 0
        # elif self.avr.defined("UCSR0B"):
        #     UCSR0B = 0
    


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

    # The callback handling for the external interrupt methods is a bit different to the original Arduino because of how
    # the Python AVR layer already handles interrupts.
    # Implementation from WInterrupts.c
    def attachInterrupt(self, interruptNum, userFunc, mode):

        avrINTx = 0

        # Configure the interrupt mode (trigger on low input, any change, rising
        # edge, or falling edge).  The mode constants were chosen to correspond
        # to the configuration bits in the hardware register, so we simply shift
        # the mode into place.

        # Enable the interrupt.

        if self.avr.defined("__AVR_ATmega32U4__"):
            # I hate doing this, but the register assignment differs between the 1280/2560
            # and the 32U4.  Since avrlib defines registers PCMSK1 and PCMSK2 that aren't
            # even present on the 32U4 this is the only way to distinguish between them.
            if interruptNum == 0:
                self.avr.EICRA = (self.avr.EICRA & invert((1<<self.avr.self.avr.ISC00) | (1<<self.avr.ISC01))) | (mode << self.avr.self.avr.ISC00)
                self.avr.self.avr.EIMSK |= (1<<self.avr.INT0)
                avrINTx = 0
            elif interruptNum == 1:
                self.avr.EICRA = (self.avr.EICRA & invert((1<<self.avr.ISC10) | (1<<self.avr.ISC11))) | (mode << self.avr.ISC10)
                self.avr.EIMSK |= (1<<self.avr.INT1)
                avrINTx = 1
            elif interruptNum == 2:
                self.avr.EICRA = (self.avr.EICRA & invert((1<<self.avr.ISC20) | (1<<self.avr.ISC21))) | (mode << self.avr.ISC20)
                self.avr.EIMSK |= (1<<self.avr.INT2)
                avrINTx = 2
            elif interruptNum == 3:
                self.avr.EICRA = (self.avr.EICRA & invert((1<<self.avr.ISC30) | (1<<self.avr.ISC31))) | (mode << self.avr.ISC30)
                self.avr.EIMSK |= (1<<self.avr.INT3)
                avrINTx = 3
            elif interruptNum == 4:
                self.avr.EICRB = (self.avr.EICRB & invert((1<<self.avr.ISC60) | (1<<self.avr.ISC61))) | (mode << self.avr.ISC60)
                self.avr.EIMSK |= (1<<self.avr.INT6)
                avrINTx = 6
        elif self.avr.defined("EICRA") and self.avr.defined("EICRB") and self.avr.defined("EIMSK"):
            if interruptNum == 2:
                self.avr.EICRA = (self.avr.EICRA & invert((1 << self.avr.ISC00) | (1 << self.avr.ISC01))) | (mode << self.avr.ISC00)
                self.avr.EIMSK |= (1 << self.avr.INT0)
                avrINTx = 0
            elif interruptNum == 3:
                self.avr.EICRA = (self.avr.EICRA & invert((1 << self.avr.ISC10) | (1 << self.avr.ISC11))) | (mode << self.avr.ISC10)
                self.avr.EIMSK |= (1 << self.avr.INT1)
                avrINTx = 1
            elif interruptNum == 4:
                self.avr.EICRA = (self.avr.EICRA & invert((1 << self.avr.ISC20) | (1 << self.avr.ISC21))) | (mode << self.avr.ISC20)
                self.avr.EIMSK |= (1 << self.avr.INT2)
                avrINTx = 2
            elif interruptNum == 5:
                self.avr.EICRA = (self.avr.EICRA & invert((1 << self.avr.ISC30) | (1 << self.avr.ISC31))) | (mode << self.avr.ISC30)
                self.avr.EIMSK |= (1 << self.avr.INT3)
                avrINTx = 3
            elif interruptNum == 0:
                self.avr.EICRB = (self.avr.EICRB & invert((1 << self.avr.ISC40) | (1 << self.avr.ISC41))) | (mode << self.avr.ISC40)
                self.avr.EIMSK |= (1 << self.avr.INT4)
                avrINTx = 4
            elif interruptNum == 1:
                self.avr.EICRB = (self.avr.EICRB & invert((1 << self.avr.ISC50) | (1 << self.avr.ISC51))) | (mode << self.avr.ISC50)
                self.avr.EIMSK |= (1 << self.avr.INT5)
                avrINTx = 5
            elif interruptNum == 6:
                self.avr.EICRB = (self.avr.EICRB & invert((1 << self.avr.ISC60) | (1 << self.avr.ISC61))) | (mode << self.avr.ISC60)
                self.avr.EIMSK |= (1 << self.avr.INT6)
                avrINTx = 6
            elif interruptNum == 7:
                self.avr.EICRB = (self.avr.EICRB & invert((1 << self.avr.ISC70) | (1 << self.avr.ISC71))) | (mode << self.avr.ISC70)
                self.avr.EIMSK |= (1 << self.avr.INT7)
                avrINTx = 7
        else:
            if interruptNum == 0:
                if self.avr.defined("EICRA") and self.avr.defined("ISC00") and self.avr.defined("EIMSK"):
                    self.avr.EICRA = (self.avr.EICRA & invert((1 << self.avr.ISC00) | (1 << self.avr.ISC01))) | (mode << self.avr.ISC00)
                    self.avr.EIMSK |= (1 << self.avr.INT0)
                elif self.avr.defined("MCUCR") and self.avr.defined("ISC00") and self.avr.defined("GICR"):
                    self.avr.MCUCR = (self.avr.MCUCR & invert((1 << self.avr.ISC00) | (1 << self.avr.ISC01))) | (mode << self.avr.ISC00)
                    self.avr.GICR |= (1 << self.avr.INT0)
                elif self.avr.defined("MCUCR") and self.avr.defined("ISC00") and self.avr.defined("GIMSK"):
                    self.avr.MCUCR = (self.avr.MCUCR & invert((1 << self.avr.ISC00) | (1 << self.avr.ISC01))) | (mode << self.avr.ISC00)
                    self.avr.GIMSK |= (1 << self.avr.INT0)
                else:
                    raise Exception("error attachInterrupt not finished for this CPU (if interruptNum == 0)")
                avrINTx = 0
            
            if interruptNum == 1:
                if self.avr.defined("EICRA") and self.avr.defined("ISC10") and self.avr.defined("ISC11") and self.avr.defined("EIMSK"):
                    self.avr.EICRA = (self.avr.EICRA & invert((1 << self.avr.ISC10) | (1 << self.avr.ISC11))) | (mode << self.avr.ISC10)
                    self.avr.EIMSK |= (1 << self.avr.INT1)
                elif self.avr.defined("MCUCR") and self.avr.defined("ISC10") and self.avr.defined("ISC11") and self.avr.defined("GICR"):
                    self.avr.MCUCR = (self.avr.MCUCR & invert((1 << self.avr.ISC10) | (1 << self.avr.ISC11))) | (mode << self.avr.ISC10)
                    self.avr.GICR |= (1 << self.avr.INT1)
                elif self.avr.defined("MCUCR") and self.avr.defined("ISC10") and self.avr.defined("GIMSK") and self.avr.defined("GIMSK"):
                    self.avr.MCUCR = (self.avr.MCUCR & invert((1 << self.avr.ISC10) | (1 << self.avr.ISC11))) | (mode << self.avr.ISC10)
                    self.avr.GIMSK |= (1 << self.avr.INT1)
                else:
                    raise Warning("warning attachself.avr.INTerrupt may need some more work for this cpu (case 1)")
                avrINTx = 1
            
            if self.avr.INTerruptNum == 2:
                if self.avr.defined("EICRA") and self.avr.defined("ISC20") and self.avr.defined("ISC21") and self.avr.defined("EIMSK"):
                    self.avr.EICRA = (self.avr.EICRA & invert((1 << self.avr.ISC20) | (1 << self.avr.ISC21))) | (mode << self.avr.ISC20)
                    self.avr.EIMSK |= (1 << self.avr.INT2)
                elif self.avr.defined("MCUCR") and self.avr.defined("ISC20") and self.avr.defined("ISC21") and self.avr.defined("GICR"):
                    self.avr.MCUCR = (self.avr.MCUCR & invert((1 << self.avr.ISC20) | (1 << self.avr.ISC21))) | (mode << self.avr.ISC20)
                    self.avr.GICR |= (1 << self.avr.INT2)
                elif self.avr.defined("MCUCR") and self.avr.defined("ISC20") and self.avr.defined("GIMSK") and self.avr.defined("GIMSK"):
                    self.avr.MCUCR = (self.avr.MCUCR & invert((1 << self.avr.ISC20) | (1 << self.avr.ISC21))) | (mode << self.avr.ISC20)
                    self.avr.GIMSK |= (1 << self.avr.INT2)
                avrINTx = 2

        if (interruptNum < self.EXTERNAL_NUM_INTERRUPTS):
            # Hook into AVR class callback system [samuelbr]
            ind = self.avr._vector_indices["INT" + str(avrINTx) + "_vect"]
            self.avr._vect[ind] = userFunc
            self.avr.enableInterrupt(ind)

    # Implementation from WInterrupts.c
    def detachInterrupt(self, interruptNum):
        if (interruptNum < self.EXTERNAL_NUM_INTERRUPTS):

            # Disable the interrupt.  (We can't assume that interruptNum is equal
            # to the number of the EIMSK bit to clear, as this isn't true on the
            # ATmega8.  There, INT0 is 6 and INT1 is 7.)

            if self.avr.defined("__AVR_ATmega32U4__"):
                if self.avr.INTerruptNum == 0:
                    self.avr.EIMSK &= ~(1<<self.avr.INT0)
                elif self.avr.INTerruptNum == 1:
                    self.avr.EIMSK &= ~(1<<self.avr.INT1)
                elif self.avr.INTerruptNum == 2:
                    self.avr.EIMSK &= ~(1<<self.avr.INT2)
                elif self.avr.INTerruptNum == 3:
                    self.avr.EIMSK &= ~(1<<self.avr.INT3)
                elif self.avr.INTerruptNum == 4:
                    self.avr.EIMSK &= ~(1<<self.avr.INT6)
            elif self.avr.defined("EICRA") and self.avr.defined("EICRB") and self.avr.defined("EIMSK"):
                if interruptNum == 2:
                    self.avr.EIMSK &= ~(1 << self.avr.INT0)                
                elif interruptNum == 3:
                    self.avr.EIMSK &= ~(1 << self.avr.INT1)
                elif interruptNum == 4:
                    self.avr.EIMSK &= ~(1 << self.avr.INT2)
                elif interruptNum == 5:
                    self.avr.EIMSK &= ~(1 << self.avr.INT3)
                elif interruptNum == 0:
                    self.avr.EIMSK &= ~(1 << self.avr.INT4)
                elif interruptNum == 1:
                    self.avr.EIMSK &= ~(1 << self.avr.INT5)
                elif interruptNum == 6:
                    self.avr.EIMSK &= ~(1 << self.avr.INT6)
                elif interruptNum == 7:
                    self.avr.EIMSK &= ~(1 << self.avr.INT7)
            else:
                if interruptNum == 0:
                    if self.avr.defined("EIMSK") and self.avr.defined("INT0"):
                        self.avr.EIMSK &= ~(1 << self.avr.INT0)
                    elif self.avr.defined("GICR") and self.avr.defined("ISC00"):
                        self.avr.GICR &= ~(1 << self.avr.INT0) # atmega32
                    elif self.avr.defined("GIMSK") and self.avr.defined("INT0"):
                        self.avr.GIMSK &= ~(1 << self.avr.INT0)
                    else:
                        raise Exception("error detachInterrupt not finished for this cpu")
                elif interruptNum == 1:
                    if self.avr.defined("EIMSK") and self.avr.defined("INT1"):
                        self.avr.EIMSK &= ~(1 << self.avr.INT1)
                    elif self.avr.defined("GICR") and self.avr.defined("INT1"):
                        self.avr.GICR &= ~(1 << self.avr.INT1) # atmega32
                    elif self.avr.defined("GIMSK") and self.avr.defined("INT1"):
                        self.avr.GIMSK &= ~(1 << self.avr.INT1)
                    else:
                        raise Warning("warning detachInterrupt may need some more work for this cpu (case 1)")

        # Hook into AVR class callback system [samuelbr]
        ind = self.avr._vector_indices["INT" + str(interruptNum) + "_vect"]
        self.avr._vect[ind] = None
        self.avr.disableInterrupt(ind)

    def interrupts(self):
        self.avr.sei()

    def noInterrupts(self):
        self.avr.cli()

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

