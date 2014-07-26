"""
leonardo.py
A port of the constants and macros in the Arduino Leonardo's 'pins_arduino.h' header.

Samuel Brian
"""

from avr import AVR, _BV
from arduino import *


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

        self.NUM_DIGITAL_PINS = 30
        self.NUM_ANALOG_INPUTS = 12

        # Mapping of analog pins as digital I/O
        # A6-A11 share with digital pins
        self.A0 = 18
        self.A1 = 19
        self.A2 = 20
        self.A3 = 21
        self.A4 = 22
        self.A5 = 23
        self.A6 = 24  # D4
        self.A7 = 25  # D6
        self.A8 = 26  # D8
        self.A9 = 27  # D9
        self.A10 = 28  # D10
        self.A11 = 29  # D12

        self.SDA = 2
        self.SCL = 3
        self.LED_BUILTIN = 13

        # Map SPI port to 'new' pins D14..D17
        self.SS = 17
        self.MOSI = 16
        self.MISO = 14
        self.SCK = 15

        self.port_to_mode_PGM = [
            Arduino.NOT_A_PORT,
            Arduino.NOT_A_PORT,
            avr.ptr("DDRB"),
            avr.ptr("DDRC"),
            avr.ptr("DDRD"),
            avr.ptr("DDRE"),
            avr.ptr("DDRF")
        ]

        self.port_to_output_PGM = [
            Arduino.NOT_A_PORT,
            Arduino.NOT_A_PORT,
            avr.ptr("PORTB"),
            avr.ptr("PORTC"),
            avr.ptr("PORTD"),
            avr.ptr("PORTE"),
            avr.ptr("PORTF")
        ]

        self.port_to_input_PGM = [
            Arduino.NOT_A_PORT,
            Arduino.NOT_A_PORT,
            avr.ptr("PINB"),
            avr.ptr("PINC"),
            avr.ptr("PIND"),
            avr.ptr("PINE"),
            avr.ptr("PINF")
        ]

        self.digital_pin_to_port_PGM = [
            Arduino.PD,  # D0 - PD2
            Arduino.PD,  # D1 - PD3
            Arduino.PD,  # D2 - PD1
            Arduino.PD,  # D3 - PD0
            Arduino.PD,  # D4 - PD4
            Arduino.PC,  # D5 - PC6
            Arduino.PD,  # D6 - PD7
            Arduino.PE,  # D7 - PE6

            Arduino.PB,  # D8 - PB4
            Arduino.PB,  # D9 - PB5
            Arduino.PB,  # D10 - PB6
            Arduino.PB,  # D11 - PB7
            Arduino.PD,  # D12 - PD6
            Arduino.PC,  # D13 - PC7

            Arduino.PB,  # D14 - MISO - PB3
            Arduino.PB,  # D15 - SCK - PB1
            Arduino.PB,  # D16 - MOSI - PB2
            Arduino.PB,  # D17 - SS - PB0

            Arduino.PF,  # D18 - A0 - PF7
            Arduino.PF,  # D19 - A1 - PF6
            Arduino.PF,  # D20 - A2 - PF5
            Arduino.PF,  # D21 - A3 - PF4
            Arduino.PF,  # D22 - A4 - PF1
            Arduino.PF,  # D23 - A5 - PF0

            Arduino.PD,  # D24 / D4 - A6 - PD4
            Arduino.PD,  # D25 / D6 - A7 - PD7
            Arduino.PB,  # D26 / D8 - A8 - PB4
            Arduino.PB,  # D27 / D9 - A9 - PB5
            Arduino.PB,  # D28 / D10 - A10 - PB6
            Arduino.PD,  # D29 / D12 - A11 - PD6
        ]

        self.digital_pin_to_bit_mask_PGM = [
            _BV(2),  # D0 - PD2
            _BV(3),  # D1 - PD3
            _BV(1),  # D2 - PD1
            _BV(0),  # D3 - PD0
            _BV(4),  # D4 - PD4
            _BV(6),  # D5 - PC6
            _BV(7),  # D6 - PD7
            _BV(6),  # D7 - PE6

            _BV(4),  # D8 - PB4
            _BV(5),  # D9 - PB5
            _BV(6),  # D10 - PB6
            _BV(7),  # D11 - PB7
            _BV(6),  # D12 - PD6
            _BV(7),  # D13 - PC7

            _BV(3),  # D14 - MISO - PB3
            _BV(1),  # D15 - SCK - PB1
            _BV(2),  # D16 - MOSI - PB2
            _BV(0),  # D17 - SS - PB0

            _BV(7),  # D18 - A0 - PF7
            _BV(6),  # D19 - A1 - PF6
            _BV(5),  # D20 - A2 - PF5
            _BV(4),  # D21 - A3 - PF4
            _BV(1),  # D22 - A4 - PF1
            _BV(0),  # D23 - A5 - PF0

            _BV(4),  # D24 / D4 - A6 - PD4
            _BV(7),  # D25 / D6 - A7 - PD7
            _BV(4),  # D26 / D8 - A8 - PB4
            _BV(5),  # D27 / D9 - A9 - PB5
            _BV(6),  # D28 / D10 - A10 - PB6
            _BV(6),  # D29 / D12 - A11 - PD6
        ]

        self.digital_pin_to_timer_PGM = [
            Arduino.NOT_ON_TIMER,
            Arduino.NOT_ON_TIMER,
            Arduino.NOT_ON_TIMER,
            Arduino.TIMER0B,  # 3
            Arduino.NOT_ON_TIMER,
            Arduino.TIMER3A,  # 5
            Arduino.TIMER4D,  # 6
            Arduino.NOT_ON_TIMER,

            Arduino.NOT_ON_TIMER,
            Arduino.TIMER1A,  # 9
            Arduino.TIMER1B,  # 10
            Arduino.TIMER0A,  # 11

            Arduino.NOT_ON_TIMER,
            Arduino.TIMER4A,  # 13

            Arduino.NOT_ON_TIMER,
            Arduino.NOT_ON_TIMER,
            Arduino.NOT_ON_TIMER,
            Arduino.NOT_ON_TIMER,
            Arduino.NOT_ON_TIMER,
            Arduino.NOT_ON_TIMER,

            Arduino.NOT_ON_TIMER,
            Arduino.NOT_ON_TIMER,
            Arduino.NOT_ON_TIMER,
            Arduino.NOT_ON_TIMER,
            Arduino.NOT_ON_TIMER,
            Arduino.NOT_ON_TIMER,
            Arduino.NOT_ON_TIMER,
            Arduino.NOT_ON_TIMER,
            Arduino.NOT_ON_TIMER,
            Arduino.NOT_ON_TIMER
        ]

        self.analog_pin_to_channel_PGM = [
            7,  # A0				PF7					ADC7
            6,  # A1				PF6					ADC6
            5,  # A2				PF5					ADC5
            4,  # A3				PF4					ADC4
            1,  # A4				PF1					ADC1
            0,  # A5				PF0					ADC0
            8,  # A6		D4		PD4					ADC8
            10,  # A7		D6		PD7					ADC10
            11,  # A8		D8		PB4					ADC11
            12,  # A9		D9		PB5					ADC12
            13,  # A10		D10		PB6					ADC13
            9  # A11		D12		PD6					ADC9
        ]

    # Macros from pins_arduino.h
    def digitalPinToPCICR(self, p):
        return self.avr.ptr("PCICR") if (
            ((p) >= 8 and (p) <= 11) or ((p) >= 14 and (p) <= 17) or ((p) >= self.A8 and (p) <= self.A10)) else None

    def digitalPinToPCICRbit(self, p):
        return 0

    def digitalPinToPCMSK(self, p):
        return self.avr.ptr("PCMSK0") if (
            ((p) >= 8 and (p) <= 11) or ((p) >= 14 and (p) <= 17) or ((p) >= self.A8 and (p) <= self.A10)) else None

    def digitalPinToPCMSKbit(self, p):
        if (p) >= 8 and (p) <= 11:
            return (p) - 4
        elif (p) == 14:
            return 3
        elif (p) == 15:
            return 1
        elif (p) == 16:
            return 2
        elif (p) == 17:
            return 0
        else:
            return p - self.A8 + 4

    def analogPinToChannel(self, P):
        return self.analog_pin_to_channel_PGM[P]

    def digitalPinToInterrupt(self, p):
        if (p) == 0:
            return 2
        elif (p) == 1:
            return 3
        elif (p) == 2:
            return 1
        elif (p) == 3:
            return 0
        elif (p) == 7:
            return 4
        else:
            return Arduino.NOT_AN_INTERRUPT
