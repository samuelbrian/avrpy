__author__ = 'samuel'

from avrpy import *

class Leonardo:

    NUM_DIGITAL_PINS  = 30
    NUM_ANALOG_INPUTS = 12

    # Mapping of analog pins as digital I/O
    # A6-A11 share with digital pins
    A0 = 18
    A1 = 19
    A2 = 20
    A3 = 21
    A4 = 22
    A5 = 23
    A6 = 24	    # D4
    A7 = 25	    # D6
    A8 = 26	    # D8
    A9 = 27	    # D9
    A10 = 28	# D10
    A11 = 29	# D12

    SDA = 2
    SCL = 3
    LED_BUILTIN = 13

    # Map SPI port to 'new' pins D14..D17
    SS   = 17
    MOSI = 16
    MISO = 14
    SCK  = 15

    PB = 2
    PC = 3
    PD = 4
    PE = 5
    PF = 6

    NOT_A_PORT = None
    NOT_ON_TIMER = None
    NOT_AN_INTERRUPT = None

    def __init__(self, avr):
        self.avr = avr

        ### Ported from leonardo/pins_arduino.h:
        self.port_to_mode_PGM = [
            Leonardo.NOT_A_PORT,
            Leonardo.NOT_A_PORT,
            avr.ptr("DDRB"),
            avr.ptr("DDRC"),
            avr.ptr("DDRD"),
            avr.ptr("DDRE"),
            avr.ptr("DDRF")
        ]

        self.port_to_output_PGM = [
            Leonardo.NOT_A_PORT,
            Leonardo.NOT_A_PORT,
            avr.ptr("PORTB"),
            avr.ptr("PORTC"),
            avr.ptr("PORTD"),
            avr.ptr("PORTE"),
            avr.ptr("PORTF")
        ]

        self.port_to_input_PGM = [
            Leonardo.NOT_A_PORT,
            Leonardo.NOT_A_PORT,
            avr.ptr("PINB"),
            avr.ptr("PINC"),
            avr.ptr("PIND"),
            avr.ptr("PINE"),
            avr.ptr("PINF")
        ]

        self.digital_pin_to_port_PGM = [
            Leonardo.PD, # D0 - PD2
            Leonardo.PD,	# D1 - PD3
            Leonardo.PD, # D2 - PD1
            Leonardo.PD,	# D3 - PD0
            Leonardo.PD,	# D4 - PD4
            Leonardo.PC, # D5 - PC6
            Leonardo.PD, # D6 - PD7
            Leonardo.PE, # D7 - PE6

            Leonardo.PB, # D8 - PB4
            Leonardo.PB,	# D9 - PB5
            Leonardo.PB, # D10 - PB6
            Leonardo.PB,	# D11 - PB7
            Leonardo.PD, # D12 - PD6
            Leonardo.PC, # D13 - PC7

            Leonardo.PB,	# D14 - MISO - PB3
            Leonardo.PB,	# D15 - SCK - PB1
            Leonardo.PB,	# D16 - MOSI - PB2
            Leonardo.PB,	# D17 - SS - PB0

            Leonardo.PF,	# D18 - A0 - PF7
            Leonardo.PF, # D19 - A1 - PF6
            Leonardo.PF, # D20 - A2 - PF5
            Leonardo.PF, # D21 - A3 - PF4
            Leonardo.PF, # D22 - A4 - PF1
            Leonardo.PF, # D23 - A5 - PF0

            Leonardo.PD, # D24 / D4 - A6 - PD4
            Leonardo.PD, # D25 / D6 - A7 - PD7
            Leonardo.PB, # D26 / D8 - A8 - PB4
            Leonardo.PB, # D27 / D9 - A9 - PB5
            Leonardo.PB, # D28 / D10 - A10 - PB6
            Leonardo.PD, # D29 / D12 - A11 - PD6
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
            Leonardo.NOT_ON_TIMER,
            Leonardo.NOT_ON_TIMER,
            Leonardo.NOT_ON_TIMER,
            avr.ptr("TIMER0B"),		# 3
            Leonardo.NOT_ON_TIMER,
            avr.ptr("TIMER3A"),		# 5
            avr.ptr("TIMER4D"),		# 6
            Leonardo.NOT_ON_TIMER,

            Leonardo.NOT_ON_TIMER,
            avr.ptr("TIMER1A"),		# 9
            avr.ptr("TIMER1B"),		# 10
            avr.ptr("TIMER0A"),		# 11

            Leonardo.NOT_ON_TIMER,
            avr.ptr("TIMER4A"),		# 13

            Leonardo.NOT_ON_TIMER,
            Leonardo.NOT_ON_TIMER,
            Leonardo.NOT_ON_TIMER,
            Leonardo.NOT_ON_TIMER,
            Leonardo.NOT_ON_TIMER,
            Leonardo.NOT_ON_TIMER,

            Leonardo.NOT_ON_TIMER,
            Leonardo.NOT_ON_TIMER,
            Leonardo.NOT_ON_TIMER,
            Leonardo.NOT_ON_TIMER,
            Leonardo.NOT_ON_TIMER,
            Leonardo.NOT_ON_TIMER,
            Leonardo.NOT_ON_TIMER,
            Leonardo.NOT_ON_TIMER,
            Leonardo.NOT_ON_TIMER,
            Leonardo.NOT_ON_TIMER
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
    def digitalPinToPCICR(self, p): return self.avr.ptr("PCICR") if (((p) >= 8 and (p) <= 11) or ((p) >= 14 and (p) <= 17) or ((p) >= Leonardo.A8 and (p) <= Leonardo.A10)) else None
    def digitalPinToPCICRbit(self, p): return 0
    def digitalPinToPCMSK(self, p): return self.avr.ptr("PCMSK0") if (((p) >= 8 and (p) <= 11) or ((p) >= 14 and (p) <= 17) or ((p) >= Leonardo.A8 and (p) <= Leonardo.A10)) else None
    def digitalPinToPCMSKbit(self, p):
        if (p) >= 8 and (p) <= 11: return (p) - 4
        elif (p) == 14: return 3
        elif (p) == 15: return 1
        elif (p) == 16: return 2
        elif (p) == 17: return 0
        else: return p - Leonardo.A8 + 4
    def analogPinToChannel(self, P): return self.analog_pin_to_channel_PGM[P]
    def digitalPinToInterrupt(self, p):
        if (p) == 0: return 2
        elif (p) == 1: return 3
        elif (p) == 2: return 1
        elif (p) == 3: return 0
        elif (p) == 7: return 4
        else: return Leonardo.NOT_AN_INTERRUPT