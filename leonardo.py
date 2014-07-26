"""
leonardo.py
A port of the constants and macros in the Arduino Leonardo's 'pins_arduino.h' header.

Samuel Brian
"""

from avr import AVR, _BV
from arduino import Arduino

class Leonardo(Arduino):
    def __init__(self, avr=None):
        if avr is None:
            avr = AVR()
            avr.parse("avrheaders/iom32u4.h")
            avr.parse("avrheaders/portpins.h")
            avr.connect()
        super().__init__(LeonardoBoard(avr))

class LeonardoBoard:

    def __init__(self, avr):
        self.avr = avr
        avr.define("F_CPU", 16000000)
        avr.define("__AVR_ATmega32U4__")

        self.NUM_DIGITAL_PINS  = 30
        self.NUM_ANALOG_INPUTS = 12

        # Mapping of analog pins as digital I/O
        # A6-A11 share with digital pins
        self.A0 = 18
        self.A1 = 19
        self.A2 = 20
        self.A3 = 21
        self.A4 = 22
        self.A5 = 23
        self.A6 = 24	    # D4
        self.A7 = 25	    # D6
        self.A8 = 26	    # D8
        self.A9 = 27	    # D9
        self.A10 = 28	    # D10
        self.A11 = 29	    # D12

        self.SDA = 2
        self.SCL = 3
        self.LED_BUILTIN = 13

        # Map SPI port to 'new' pins D14..D17
        self.SS   = 17
        self.MOSI = 16
        self.MISO = 14
        self.SCK  = 15

        # These are actually defined in Arduino.h
        self.PB = 2
        self.PC = 3
        self.PD = 4
        self.PE = 5
        self.PF = 6
        self.NOT_A_PORT = 0
        self.NOT_A_PIN = 0
        self.NOT_ON_TIMER = 0
        self.NOT_AN_INTERRUPT = -1

        self.port_to_mode_PGM = [
            self.NOT_A_PORT,
            self.NOT_A_PORT,
            avr.ptr("DDRB"),
            avr.ptr("DDRC"),
            avr.ptr("DDRD"),
            avr.ptr("DDRE"),
            avr.ptr("DDRF")
        ]

        self.port_to_output_PGM = [
            self.NOT_A_PORT,
            self.NOT_A_PORT,
            avr.ptr("PORTB"),
            avr.ptr("PORTC"),
            avr.ptr("PORTD"),
            avr.ptr("PORTE"),
            avr.ptr("PORTF")
        ]

        self.port_to_input_PGM = [
            self.NOT_A_PORT,
            self.NOT_A_PORT,
            avr.ptr("PINB"),
            avr.ptr("PINC"),
            avr.ptr("PIND"),
            avr.ptr("PINE"),
            avr.ptr("PINF")
        ]

        self.digital_pin_to_port_PGM = [
            self.PD, # D0 - PD2
            self.PD,	# D1 - PD3
            self.PD, # D2 - PD1
            self.PD,	# D3 - PD0
            self.PD,	# D4 - PD4
            self.PC, # D5 - PC6
            self.PD, # D6 - PD7
            self.PE, # D7 - PE6

            self.PB, # D8 - PB4
            self.PB,	# D9 - PB5
            self.PB, # D10 - PB6
            self.PB,	# D11 - PB7
            self.PD, # D12 - PD6
            self.PC, # D13 - PC7

            self.PB,	# D14 - MISO - PB3
            self.PB,	# D15 - SCK - PB1
            self.PB,	# D16 - MOSI - PB2
            self.PB,	# D17 - SS - PB0

            self.PF,	# D18 - A0 - PF7
            self.PF, # D19 - A1 - PF6
            self.PF, # D20 - A2 - PF5
            self.PF, # D21 - A3 - PF4
            self.PF, # D22 - A4 - PF1
            self.PF, # D23 - A5 - PF0

            self.PD, # D24 / D4 - A6 - PD4
            self.PD, # D25 / D6 - A7 - PD7
            self.PB, # D26 / D8 - A8 - PB4
            self.PB, # D27 / D9 - A9 - PB5
            self.PB, # D28 / D10 - A10 - PB6
            self.PD, # D29 / D12 - A11 - PD6
        ]

        self.digital_pin_to_bit_mask_PGM = [
            _BV(2), # D0 - PD2
            _BV(3),	# D1 - PD3
            _BV(1), # D2 - PD1
            _BV(0),	# D3 - PD0
            _BV(4),	# D4 - PD4
            _BV(6), # D5 - PC6
            _BV(7), # D6 - PD7
            _BV(6), # D7 - PE6
            
            _BV(4), # D8 - PB4
            _BV(5),	# D9 - PB5
            _BV(6), # D10 - PB6
            _BV(7),	# D11 - PB7
            _BV(6), # D12 - PD6
            _BV(7), # D13 - PC7
            
            _BV(3),	# D14 - MISO - PB3
            _BV(1),	# D15 - SCK - PB1
            _BV(2),	# D16 - MOSI - PB2
            _BV(0),	# D17 - SS - PB0
            
            _BV(7),	# D18 - A0 - PF7
            _BV(6), # D19 - A1 - PF6
            _BV(5), # D20 - A2 - PF5
            _BV(4), # D21 - A3 - PF4
            _BV(1), # D22 - A4 - PF1
            _BV(0), # D23 - A5 - PF0
            
            _BV(4), # D24 / D4 - A6 - PD4
            _BV(7), # D25 / D6 - A7 - PD7
            _BV(4), # D26 / D8 - A8 - PB4
            _BV(5), # D27 / D9 - A9 - PB5
            _BV(6), # D28 / D10 - A10 - PB6
            _BV(6), # D29 / D12 - A11 - PD6
        ]

        self.digital_pin_to_timer_PGM = [
            self.NOT_ON_TIMER,
            self.NOT_ON_TIMER,
            self.NOT_ON_TIMER,
            avr.ptr("TIMER0B"),		# 3
            self.NOT_ON_TIMER,
            avr.ptr("TIMER3A"),		# 5
            avr.ptr("TIMER4D"),		# 6
            self.NOT_ON_TIMER,

            self.NOT_ON_TIMER,
            avr.ptr("TIMER1A"),		# 9
            avr.ptr("TIMER1B"),		# 10
            avr.ptr("TIMER0A"),		# 11

            self.NOT_ON_TIMER,
            avr.ptr("TIMER4A"),		# 13

            self.NOT_ON_TIMER,
            self.NOT_ON_TIMER,
            self.NOT_ON_TIMER,
            self.NOT_ON_TIMER,
            self.NOT_ON_TIMER,
            self.NOT_ON_TIMER,

            self.NOT_ON_TIMER,
            self.NOT_ON_TIMER,
            self.NOT_ON_TIMER,
            self.NOT_ON_TIMER,
            self.NOT_ON_TIMER,
            self.NOT_ON_TIMER,
            self.NOT_ON_TIMER,
            self.NOT_ON_TIMER,
            self.NOT_ON_TIMER,
            self.NOT_ON_TIMER
        ]

        self.analog_pin_to_channel_PGM = [
            7,	# A0				PF7					ADC7
            6,	# A1				PF6					ADC6
            5,	# A2				PF5					ADC5
            4,	# A3				PF4					ADC4
            1,	# A4				PF1					ADC1
            0,	# A5				PF0					ADC0
            8,	# A6		D4		PD4					ADC8
            10,	# A7		D6		PD7					ADC10
            11,	# A8		D8		PB4					ADC11
            12,	# A9		D9		PB5					ADC12
            13,	# A10		D10		PB6					ADC13
            9	# A11		D12		PD6					ADC9
        ]

    # Macros from pins_arduino.h
    def digitalPinToPCICR(self, p): return self.avr.ptr("PCICR") if (((p) >= 8 and (p) <= 11) or ((p) >= 14 and (p) <= 17) or ((p) >= self.A8 and (p) <= self.A10)) else None
    def digitalPinToPCICRbit(self, p): return 0
    def digitalPinToPCMSK(self, p): return self.avr.ptr("PCMSK0") if (((p) >= 8 and (p) <= 11) or ((p) >= 14 and (p) <= 17) or ((p) >= self.A8 and (p) <= self.A10)) else None
    def digitalPinToPCMSKbit(self, p):
        if (p) >= 8 and (p) <= 11: return (p) - 4
        elif (p) == 14: return 3
        elif (p) == 15: return 1
        elif (p) == 16: return 2
        elif (p) == 17: return 0
        else: return p - self.A8 + 4
    def analogPinToChannel(self, P): return self.analog_pin_to_channel_PGM[P]
    def digitalPinToInterrupt(self, p):
        if (p) == 0: return 2
        elif (p) == 1: return 3
        elif (p) == 2: return 1
        elif (p) == 3: return 0
        elif (p) == 7: return 4
        else: return self.NOT_AN_INTERRUPT
