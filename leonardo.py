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


        # avr._SFR_IO8 = {'SPSR': 45, 'GPIOR1': 42, 'PORTD': 11, 'ACSR': 48, 'PINB': 3, 'OCR0B': 40, 'PCIFR': 27, 'SPCR': 44, 'DDRF': 16, 'DDRB': 4, 'TIFR4': 25, 'PORTB': 5, 'TIFR0': 21, 'TCCR0A': 36, 'PINC': 6, 'DDRC': 7, 'TCNT0': 38, 'PLLCSR': 41, 'EECR': 31, 'PINE': 12, 'OCDR': 49, 'EIND': 60, 'TIFR5': 26, 'SMCR': 51, 'PORTC': 8, 'GPIOR2': 43, 'DDRD': 10, 'PORTE': 14, 'PLLFRQ': 50, 'TIFR1': 22, 'EEDR': 32, 'PORTF': 17, 'SPDR': 46, 'TIFR3': 24, 'RAMPZ': 59, 'TCCR0B': 37, 'EIFR': 28, 'OCR0A': 39, 'TIFR2': 23, 'EEARL': 33, 'MCUSR': 52, 'EIMSK': 29, 'MCUCR': 53, 'EEARH': 34, 'PIND': 9, 'DDRE': 13, 'GTCCR': 35, 'PINF': 15, 'GPIOR0': 30, 'SPMCSR': 55}
        # avr._SFR_IO16 = {'EEAR': 33}
        # avr._SFR_MEM8 = {'OCR4C': 209, 'UCSR1B': 201, 'TIMSK0': 110, 'UEDATX': 241, 'RCCTRL': 103, 'UENUM': 233, 'OCR3AL': 152, 'ADCSRA': 122, 'OCR1AL': 136, 'TCCR1B': 129, 'TIMSK1': 111, 'CLKSEL1': 198, 'UDFNUML': 228, 'EICRA': 105, 'DIDR2': 125, 'OCR3AH': 153, 'PCICR': 104, 'DIDR1': 127, 'UDR1': 206, 'OCR1CL': 140, 'UERST': 234, 'UDINT': 225, 'WDTCSR': 96, 'OCR4A': 207, 'OCR4D': 210, 'TCCR2A': 176, 'CLKSEL0': 197, 'TCNT3H': 149, 'OCR3CH': 157, 'OCR3BL': 154, 'USBCON': 216, 'UPCFG2X': 173, 'TCNT3L': 148, 'ADCL': 120, 'DT4': 212, 'TCCR4A': 192, 'UHFLEN': 164, 'TC4H': 191, 'UEBCHX': 243, 'TCCR3B': 145, 'ADCSRB': 123, 'UDMFN': 230, 'TIMSK5': 115, 'ICR1L': 134, 'UECFG1X': 237, 'PRR1': 101, 'TCCR2B': 177, 'ICR1H': 135, 'UPRST': 168, 'UPNUM': 167, 'UPINRQX': 165, 'UPIENX': 174, 'TIMSK3': 113, 'UDIEN': 226, 'USBSTA': 217, 'UESTA1X': 239, 'PCMSK1': 108, 'UDCON': 224, 'UCSR1C': 202, 'UECFG0X': 236, 'TCCR1A': 128, 'TCCR1C': 130, 'OTGIEN': 222, 'DIDR0': 126, 'UHINT': 159, 'TWCR': 188, 'UDFNUMH': 229, 'TCCR3C': 146, 'TCNT1L': 132, 'TIMSK2': 112, 'ICR3L': 150, 'OCR4B': 208, 'OCR2B': 180, 'UHFNUML': 162, 'OCR1CH': 141, 'CLKSTA': 199, 'UDADDR': 227, 'OCR1BH': 139, 'UDTST': 231, 'UHFNUMH': 163, 'OTGINT': 223, 'UPCFG1X': 171, 'UHIEN': 160, 'PRR0': 100, 'OCR2A': 179, 'EICRB': 106, 'UPINTX': 166, 'TCCR4B': 193, 'UPBCLX': 246, 'TWSR': 185, 'OCR1BL': 138, 'TWBR': 184, 'OTGTCON': 249, 'UCSR1A': 200, 'UEBCLX': 242, 'UPINT': 248, 'TWAMR': 189, 'TCNT1H': 133, 'TCNT4L': 190, 'OSCCAL': 102, 'TCCR4D': 195, 'UHCON': 158, 'TCCR4C': 194, 'USBINT': 218, 'UBRR1H': 205, 'TCCR4E': 196, 'TWDR': 187, 'UPDATX': 175, 'ADMUX': 124, 'UPCFG0X': 170, 'UPCONX': 169, 'ADCH': 121, 'TCNT4H': 191, 'UEIENX': 240, 'PCMSK2': 109, 'TIMSK4': 114, 'TWAR': 186, 'UHADDR': 161, 'PCMSK0': 107, 'OCR1AH': 137, 'UEINTX': 232, 'UECONX': 235, 'OCR3CL': 156, 'UHWCON': 215, 'UEINT': 244, 'ICR3H': 151, 'TCCR3A': 144, 'UPERRX': 245, 'TCNT2': 178, 'OTGCON': 221, 'UPSTAX': 172, 'UPBCHX': 247, 'UBRR1L': 204, 'UESTA0X': 238, 'OCR3BH': 155, 'CLKPR': 97}
        # avr._SFR_MEM16 = {'UDFNUM': 228, 'TCNT4': 190, 'UHFNUM': 162, 'OCR3B': 154, 'UBRR1': 204, 'ICR3': 150, 'ICR1': 134, 'OCR1C': 140, 'UEBCX': 242, 'ADC': 120, 'TCNT3': 148, 'OCR3A': 152, 'OCR1A': 136, 'TCNT1': 132, 'OCR1B': 138, 'OCR3C': 156}
        # avr._constants = {'WGM20': 0, 'FOC2B': 6, 'COM1A1': 7, 'EEAR7': 7, 'PORTD0': 0, 'CLKS': 0, 'CAL4': 4, 'COM3A1': 7, 'TWBR6': 6, 'PINF5': 5, 'EPSIZE1': 5, 'OCR3CH3': 3, 'OCR1CL4': 4, 'BYCT6': 6, 'ICNC1': 7, 'WGM33': 4, 'ICIE3': 5, 'RAMPZ0': 0, 'EXSUT1': 5, 'OCR1CL6': 6, 'ICR1H5': 5, 'PIND7': 7, 'PDIV2': 2, 'OCR4D6': 6, 'TC48': 0, 'OCR3CH1': 1, 'OCR4D2': 2, 'TC49': 1, 'RCSUT1': 7, 'CS31': 1, 'UDR1_4': 4, 'PLLUSB': 6, 'SUSPI': 0, 'CURRBK0': 0, 'OCR1AL2': 2, 'ADHSM': 7, 'TCNT1L1': 1, 'INTF2': 2, 'OCR0B_0': 0, 'EPINT4': 4, 'OCR4D7': 7, 'OCR4A5': 5, 'DAT3': 3, 'OCR3BH4': 4, 'OCR1AH0': 0, 'EPRST0': 0, 'ICR1H1': 1, 'OCR3CH0': 0, 'PORTD5': 5, 'COM3C0': 2, 'ADC9D': 1, 'PWM4D': 0, 'GPIOR05': 5, 'OCR3CL1': 1, 'SM1': 2, 'EEPM1': 5, 'GPIOR20': 0, 'CS01': 1, 'EPRST5': 5, 'ICNC3': 7, 'DDC6': 6, 'COM1C0': 2, 'OCR3BH5': 5, 'FE1': 4, 'INTF0': 0, 'PRTIM3': 3, 'OCDR2': 2, 'INT7': 7, 'ADCL6': 6, 'EPEN': 0, 'OCR1AL7': 7, 'ICR3L2': 2, 'PRUSART0': 1, 'ADTS1': 1, 'OCIE4A': 6, 'FOC4D': 1, 'PIND1': 1, 'OCR0B_7': 7, 'OCR1BL0': 0, 'EPINT5': 5, 'ICR3L5': 5, 'OC4OE4': 4, 'OC4OE2': 2, 'OCDR1': 1, 'ENHC4': 6, 'ICR1H0': 0, 'SPDR4': 4, 'INT6': 6, 'PRUSART1': 0, 'SOFE': 2, 'SIGRD': 5, 'ISC20': 4, 'OCR0A_4': 4, 'TCNT3L3': 3, 'PINC7': 7, 'TXEN1': 3, 'ADCL7': 7, 'OCR1BH4': 4, 'OCR3BL5': 5, 'PGERS': 1, 'SPDR6': 6, 'PSRASY': 1, 'FPIE4': 7, 'DT4L5': 5, 'PIND2': 2, 'TCNT1L6': 6, 'FPEN4': 6, 'PORTF7': 7, 'ICES3': 6, 'UADD0': 0, 'OCR1BH3': 3, 'INTF4': 4, 'INTF1': 1, 'PORTB6': 6, 'PINF0': 0, 'OCR1BL3': 3, 'BYCT2': 2, 'RCON': 1, 'TWD3': 3, 'ADCL5': 5, 'OCIE3C': 3, 'PIND5': 5, 'EEDR4': 4, 'PWM4X': 7, 'FOC3C': 5, 'EPRST2': 2, 'OCR1CH4': 4, 'ALLOC': 1, 'OCR4B6': 6, 'FNCERR': 4, 'TWD6': 6, 'GPIOR23': 3, 'PCINT0': 0, 'WGM41': 1, 'TCNT0_7': 7, 'WDCE': 4, 'PRSPI': 2, 'EEDR2': 2, 'OCR1AH2': 2, 'COM2B1': 5, 'FOC3A': 7, 'PINF6': 6, 'ADC12D': 4, 'RCSUT0': 6, 'PINMUX': 7, 'BYCT7': 7, 'PINF7': 7, 'TCNT1L7': 7, 'DAT0': 0, 'ADC1D': 1, 'DDD2': 2, 'OCIE0B': 2, 'GPIOR04': 4, 'TWAM2': 3, 'SM2': 3, 'EEAR4': 4, 'ICR1L7': 7, 'ICR3H0': 0, 'OCDR0': 0, 'VBUSTI': 0, 'COM2A0': 6, 'PINB4': 4, 'GPIOR22': 2, 'ADC8D': 0, 'OCR0B_3': 3, 'PGWRT': 2, 'OCR1CH7': 7, 'FOC0B': 6, 'FOC1C': 5, 'SPDR7': 7, 'PUD': 4, 'TWA4': 5, 'OCR2_0': 0, 'DDD4': 4, 'PWM4A': 1, 'DT4L7': 7, 'RCFREQ': 0, 'ICR3H4': 4, 'PLLTM0': 4, 'OCR1CL3': 3, 'FNUM10': 2, 'EIND0': 0, 'WGM10': 0, 'WDP0': 0, 'DAT1': 1, 'OCR1BH5': 5, 'DDC7': 7, 'ADCH7': 7, 'FUSE_MEMORY_SIZE': 3, 'PRTIM2': 6, 'ADPS2': 2, 'OCR1AL3': 3, 'PINB3': 3, 'ICR3H3': 3, 'OCR4A3': 3, 'OCR3AH6': 6, 'OCR0A_0': 0, 'EPBK1': 3, 'OCR4A1': 1, 'JTRF': 4, 'FOC4A': 3, 'TC42': 2, 'OCF1A': 1, 'DDE2': 2, 'TWAM0': 1, 'WGM30': 0, 'PORTF5': 5, 'CAL7': 7, 'TCNT1H3': 3, 'TWBR3': 3, 'GPIOR03': 3, 'ICR1H2': 2, 'ISC50': 2, 'UADD2': 2, 'ACO': 5, 'TWBR7': 7, 'COM2B0': 4, 'JTD': 7, 'GPIOR26': 6, 'ISC71': 7, 'OCR4D3': 3, 'FOC4B': 2, 'TLOCK4': 7, 'GPIOR14': 4, 'PORTE6': 6, 'ADC7D': 7, 'PINF1': 1, 'CS42': 2, 'REFS1': 7, 'OCR1CH0': 0, 'ADCL1': 1, 'TOIE3': 0, 'WDP2': 2, 'OCR3BL6': 6, 'OCR3CL6': 6, 'EEAR0': 0, 'EEDR0': 0, 'OCF3A': 1, 'TOV1': 0, 'TWBR4': 4, '__BOOT_LOCK_BITS_1_EXIST': None, 'AIN0D': 0, 'TWAM5': 6, 'EXTON': 0, 'EPRST1': 1, 'GPIOR02': 2, 'FOC1A': 7, 'WGM02': 3, 'PINE2': 2, 'OCR1AL5': 5, 'OCR1AH3': 3, 'ADCH0': 0, 'TWD0': 0, 'TCNT2_3': 3, 'FNUM1': 1, 'WGM13': 4, 'OCR1BH7': 7, 'PWM4B': 0, 'WDE': 3, 'ADC13D': 5, 'UDR1_1': 1, 'OCF4D': 7, 'WGM31': 1, 'TWD5': 5, 'OCR1AH1': 1, 'EPINT3': 3, 'ISC60': 4, 'OCR2_1': 1, 'ADC5D': 5, 'BORF': 2, 'PDIV3': 3, 'ICR1L5': 5, 'CLKPS0': 0, 'TWBR5': 5, 'OCR4C5': 5, 'TWAM4': 5, 'OCR4C7': 7, 'BYCT4': 4, 'DDD7': 7, 'RCCKSEL3': 7, 'OCR3BL4': 4, 'EPINT2': 2, 'TCNT1H7': 7, 'BYCT1': 1, 'OCR4C1': 1, 'DDB3': 3, 'RXB81': 1, 'OCR3BH1': 1, 'OCR3CL5': 5, 'INT0': 0, 'COM3B1': 5, '__BOOT_LOCK_BITS_0_EXIST': None, 'CLKPCE': 7, 'OCR2_3': 3, 'CS43': 3, 'EXCKSEL3': 3, 'TCNT3H3': 3, 'DT4L3': 3, 'PINB1': 1, 'OCR3AL7': 7, 'FIFOCON': 7, 'ICR3L4': 4, 'TCNT1H6': 6, 'OCR4B0': 0, 'PINB0': 0, 'SPIF': 7, 'ADTS3': 4, 'ICR3L1': 1, 'PDIV0': 0, 'MUX2': 2, 'OCR0B_2': 2, 'TWS5': 5, 'STALLEDE': 1, 'TCNT1L4': 4, 'TSM': 7, 'ADCL2': 2, 'ADC2D': 2, 'CLKPS1': 1, 'ICR3L3': 3, 'OCF1C': 3, 'OCR3AL3': 3, 'PRTIM1': 3, 'OCR1BL5': 5, 'FOC3B': 6, 'OCR0B_6': 6, 'PCINT5': 5, 'TCNT0_0': 0, 'DDD1': 1, 'PORTD7': 7, 'GPIOR16': 6, 'ADCL4': 4, 'CS20': 0, 'TWINT': 7, 'SIGNATURE_1': 149, 'EXTE': 2, 'CS11': 1, 'INT4': 4, 'EEAR11': 3, 'CFGOK': 7, 'OCIE3B': 2, 'TWPS0': 0, 'TCNT3L6': 6, 'OCR3AL6': 6, 'TWSTO': 4, 'WDIF': 7, 'TC45': 5, 'OCR3AH5': 5, 'OC4OE1': 1, 'F_CPU': 16000000, 'WGM11': 1, 'COM4D0': 2, 'TCNT3H0': 0, 'ADTS0': 0, 'FNUM0': 0, 'INT1': 1, 'PIND4': 4, 'ISC01': 1, 'OCR2_6': 6, 'LSM': 2, 'TCNT1L3': 3, 'BLBSET': 3, 'OCR3AL1': 1, 'COM4B0': 4, 'PCINT6': 6, 'GPIOR27': 7, 'UADD4': 4, 'OCR4C3': 3, 'EXCKSEL0': 0, 'RXC1': 7, 'OCR4B1': 1, 'TCNT2_7': 7, 'UDR1_5': 5, 'BYCT5': 5, 'PRTWI': 7, 'OCR3CH5': 5, 'TWA5': 6, 'EEDR1': 1, 'DDB4': 4, 'COM1B1': 5, 'OCR1BH0': 0, 'STALLEDI': 1, 'ICR3H6': 6, 'OCR4D1': 1, 'TWAM1': 2, 'REFS0': 6, 'PLOCK': 0, 'TCNT3H5': 5, 'NBUSYBK1': 1, 'OCR3CL3': 3, 'EPTYPE1': 7, 'GPIOR15': 5, 'OCR3AH3': 3, 'COM1B0': 4, 'DAT4': 4, 'COM4A1': 7, 'OCIE1C': 3, 'ICR1L2': 2, 'OCR4C0': 0, 'CTRLDIR': 2, 'CURRBK1': 1, 'ISC41': 1, 'RWWSRE': 4, 'DTPS41': 5, 'OCR0B_4': 4, 'PINF4': 4, 'TWGCE': 0, 'CS00': 0, 'RXSTPE': 3, 'INT5': 5, 'FNUM3': 3, 'TC44': 4, 'EPSIZE0': 4, 'TXCIE1': 6, 'COM4A1S': 7, 'ADDEN': 7, 'SPDR2': 2, 'EEAR2': 2, 'OCR4A0': 0, 'OCR4B7': 7, 'CAL0': 0, 'CS41': 1, 'OCR1BL4': 4, 'TCNT3L1': 1, 'ADPS0': 0, 'OCR3CH2': 2, 'OCR1AH7': 7, 'IVSEL': 1, 'EEAR3': 3, 'RXSTPI': 3, 'BYCT3': 3, 'MUX3': 3, 'TCNT3H1': 1, 'COM1A0': 6, 'UADD3': 3, 'PINE6': 6, 'MUX5': 5, 'EEPM0': 4, 'OCIE1B': 2, 'WGM12': 3, 'CS30': 0, 'TWD7': 7, 'TXINE': 0, 'TCNT3H4': 4, 'OC4OE0': 0, 'STALLRQC': 4, 'RCCKSEL2': 6, 'TWPS1': 1, 'OCR4B4': 4, 'PORTB3': 3, 'INTF7': 7, 'ISC61': 5, 'WDIE': 6, 'TWS6': 6, 'TWIE': 0, 'OCF4A': 6, 'UPM11': 5, 'PIND6': 6, 'TCNT2_4': 4, 'DAT6': 6, 'TCNT1L2': 2, 'UMSEL10': 6, 'ADCH4': 4, 'SIGNATURE_0': 30, 'OCR0A_1': 1, 'EEAR5': 5, 'DDB1': 1, 'TOIE1': 0, 'WCOL': 6, 'SPR1': 1, 'OCIE4B': 5, 'ACME': 6, 'OCR3CL2': 2, 'U2X1': 1, 'OCR4D4': 4, 'EPBK0': 2, 'TWA6': 7, 'PORTD1': 1, 'OCR1AL4': 4, 'WDP1': 1, 'TOIE0': 0, 'ADC0D': 0, 'GPIOR13': 3, 'TCNT0_3': 3, 'EEAR10': 2, 'EXCKSEL2': 2, 'CAL1': 1, 'SPR0': 0, 'DDF6': 6, 'DORD': 5, 'OCR3BH0': 0, 'PIND0': 0, 'EXTRF': 1, 'OCR3BL1': 1, 'SPIE': 7, 'RXOUTI': 2, 'DDB5': 5, 'TCNT3H7': 7, 'TCNT1H0': 0, 'OCR1CL0': 0, 'SPDR1': 1, 'PCINT1': 1, 'OCDR4': 4, 'DDD5': 5, 'UPRSMI': 6, 'TCNT1H4': 4, 'TCNT1H2': 2, 'RXCIE1': 7, 'AIN1D': 1, 'ISC00': 0, 'PCINT2': 2, 'TCNT0_4': 4, 'PORTB5': 5, 'TCNT2_6': 6, 'COM4D1': 3, 'CS21': 1, 'OCR3CL7': 7, 'ICR3H5': 5, 'GPIOR11': 1, 'IVCE': 0, 'VBUSTE': 0, 'EEAR8': 0, 'ISC31': 7, 'SUSPE': 0, 'TCNT2_1': 1, 'OCR2_4': 4, 'OCIE2B': 2, 'PORTB2': 2, 'EPINT6': 6, 'INTF6': 6, 'OCF3C': 3, 'OCR3AH7': 7, 'PRUSB': 7, 'OCR4B3': 3, 'OCR3AH4': 4, 'OCR3BH7': 7, 'RCCKSEL0': 4, 'GPIOR24': 4, 'TWD2': 2, 'PORTC6': 6, 'TXINI': 0, 'OCIE3A': 1, 'ADC11D': 3, 'TCNT2_5': 5, 'DDB7': 7, 'DTPS40': 4, 'OCR0B_5': 5, 'INT3': 3, 'DDB6': 6, 'COM4B1S': 5, 'WGM00': 0, 'SIGNATURE_2': 135, 'PLLTM1': 5, 'UVREGE': 0, 'WAKEUPE': 4, 'TCNT0_5': 5, 'DDF5': 5, 'FNUM9': 1, 'TOV2': 0, 'EEAR6': 6, 'EPINT0': 0, 'CS12': 2, 'EERIE': 3, 'RSTDT': 3, 'CS10': 0, 'PORTF6': 6, 'NAKOUTE': 4, 'FNUM2': 2, 'COM0A0': 6, 'PORTF0': 0, 'OCR1CH6': 6, 'OCR4B5': 5, 'CLKPS3': 3, 'WGM32': 3, 'CLKPS2': 2, 'ADC10D': 2, 'OCR1CL7': 7, 'GPIOR00': 0, 'ICF3': 5, 'BYCT0': 0, 'OCF0A': 1, 'WGM01': 1, 'TCNT3L0': 0, 'CS32': 2, 'ACIS0': 0, 'ADC6D': 6, 'OCR3BL3': 3, 'ISC11': 3, 'EPINT1': 1, 'GPIOR12': 2, 'ADCH1': 1, 'OCDR3': 3, 'EPRST4': 4, 'TWA2': 3, 'RWWSB': 6, 'OCR4C6': 6, 'OCR0A_2': 2, 'ICR3L0': 0, 'EEAR9': 1, 'UDRE1': 5, 'OCR4D5': 5, 'PINB2': 2, 'UCSZ11': 2, 'PORTB4': 4, 'ADCL3': 3, 'FOC0A': 7, 'TCNT3L5': 5, 'TOIE4': 2, 'ICR1L0': 0, 'OCR2_7': 7, 'ACIE': 3, 'OCIE4D': 7, 'PORTE2': 2, 'ISC51': 3, 'RCCKSEL1': 5, 'WDRF': 3, 'ADC3D': 3, 'TWA1': 2, 'FNUM4': 4, 'EEMPE': 2, 'ICR3L6': 6, 'PCINT3': 3, 'DDD3': 3, 'OCR3AL2': 2, 'UENUM_2': 2, 'ICIE1': 5, 'TWWC': 3, 'OCR3BH6': 6, 'PORTF1': 1, 'SPMEN': 0, 'UDR1_2': 2, 'SE': 0, 'DDD6': 6, 'INTF3': 3, 'DT4L2': 2, 'ADCH6': 6, 'MUX4': 4, 'EPSIZE2': 6, 'OCR1AL1': 1, 'TWS3': 3, 'ICR1H3': 3, 'PORTB1': 1, 'EEPE': 1, 'COM4B0S': 4, 'PINB6': 6, 'TC410': 2, 'EXSUT0': 4, 'FNUM5': 5, 'ISC70': 6, 'WGM21': 1, 'TCNT1H5': 5, 'TC40': 0, 'UDR1_6': 6, 'CAL6': 6, 'GPIOR01': 1, 'INTF5': 5, 'PDIV1': 1, 'TWBR0': 0, 'OCR3CH6': 6, 'SPE': 6, 'OCR1CL2': 2, 'PORTD2': 2, 'OCDR6': 6, 'OCF3B': 2, 'TCNT2_0': 0, 'FLERRE': 7, 'PIND3': 3, 'TCNT0_6': 6, 'OCR3CL0': 0, 'EPDIR': 0, 'FOC2A': 7, 'OVERFI': 6, 'EPRST6': 6, 'TXB81': 0, 'ICR1H7': 7, 'EXCKSEL1': 1, 'CS02': 2, 'ADCH5': 5, 'ADATE': 5, 'OCR1BL1': 1, '_AVR_IOM32U4_H_': 1, 'OCR4D0': 0, 'PRADC': 0, 'OCR0B_1': 1, 'FPAC4': 3, 'DDB2': 2, 'OCIE1A': 1, 'DT4L6': 6, 'OCR0A_6': 6, 'FNUM8': 0, 'OCR1AH6': 6, 'ISC40': 0, 'DAT7': 7, 'COM3C1': 3, 'FNUM7': 7, 'TCNT3L7': 7, 'WAKEUPI': 4, 'OCF2B': 2, 'TC47': 7, 'TC46': 6, 'ACD': 7, 'PORTC7': 7, 'ICR1L1': 1, 'TWBR2': 2, 'OCR3CL4': 4, 'DDF1': 1, 'ADLAR': 5, 'FPES4': 4, 'ICR3H7': 7, 'ICR3H2': 2, 'TOV4': 2, 'RXOUTE': 2, 'COM4B1': 5, 'OCR1AL6': 6, 'EORSME': 5, 'TWS4': 4, 'MUX0': 0, 'PSRSYNC': 0, 'PCIE0': 0, 'NAKINE': 6, 'SM0': 1, 'OCR1BH2': 2, 'OCR3AL4': 4, 'FRZCLK': 5, 'TOIE2': 0, 'CPHA': 2, 'GPIOR17': 7, 'OCF1B': 2, 'ADIF': 4, 'OCR3AH0': 0, 'WGM40': 0, 'OCR3CH7': 7, 'NAKOUTI': 4, 'EORSTI': 3, 'MUX1': 1, 'PLLE': 1, '__LOCK_BITS_EXIST': None, 'TWAM3': 4, 'OCR1CH3': 3, 'OCF0B': 2, 'ICR1H4': 4, 'ISC21': 5, 'COM0A1': 7, 'PINDIV': 4, 'UENUM_0': 0, 'PINC6': 6, 'OCR1BL2': 2, 'PORTB0': 0, 'ADPS1': 1, 'ADIE': 3, 'OCR1CH5': 5, 'OCR4A6': 6, 'RXEN1': 4, 'RMWKUP': 1, 'COM1C1': 3, 'TWBR1': 1, 'COM4A0S': 6, 'ACIC': 2, 'UADD6': 6, 'OCR3AL0': 0, 'OTGPADE': 4, 'UADD1': 1, 'SPDR5': 5, 'OCR0A_3': 3, 'EEDR6': 6, 'OCR1AH4': 4, 'OCR3BH3': 3, 'ADTS2': 2, 'PINB5': 5, 'TWS7': 7, 'DOR1': 3, 'TOV3': 0, 'UPM10': 4, 'OCR2_2': 2, 'OCR1AL0': 0, 'DDF7': 7, 'ICR1L3': 3, 'OCR0A_7': 7, 'TWSTA': 5, 'OCR4B2': 2, 'ACIS1': 1, 'CAL3': 3, 'OCR4A4': 4, 'OCR4C2': 2, 'OCR4C4': 4, 'FNUM6': 6, 'SOFI': 2, 'NBUSYBK0': 0, 'OCR1AH5': 5, 'OCR1BL6': 6, 'UDR1_0': 0, 'ADCL0': 0, 'GPIOR06': 6, 'PINB7': 7, 'ISC30': 6, 'DT4L4': 4, 'TCNT1H1': 1, 'VBUS': 0, 'PORTD3': 3, 'DDD0': 0, 'ICES1': 6, 'OCR1CH1': 1, 'OCR2_5': 5, 'TCNT1L5': 5, 'EEDR3': 3, 'DETACH': 0, 'OCR3BH2': 2, 'OCF4B': 5, 'DT4L1': 1, 'PORTB7': 7, 'COM3B0': 4, 'COM4A0': 6, 'UENUM_1': 1, 'FPF4': 2, 'TWD1': 1, 'PRTIM0': 5, 'OCR3BL0': 0, 'OCR1BH6': 6, 'TWEN': 2, 'CAL5': 5, 'OCR4A2': 2, 'UNDERFI': 5, 'GPIOR07': 7, 'DAT2': 2, 'FPNC4': 5, 'EPTYPE0': 6, 'ADC4D': 4, 'NAKINI': 6, 'DAT5': 5, 'DTSEQ1': 3, 'DTSEQ0': 2, 'OCR3AH2': 2, '__AVR_ATmega32U4__': None, 'OCR1CL5': 5, 'UPE1': 2, 'TCNT1L0': 0, 'OCDR7': 7, 'ADEN': 7, '_AVR_PORTPINS_H_': 1, 'UDRIE1': 5, 'PSR4': 6, 'TCNT3H6': 6, 'SPMIE': 7, 'DT4L0': 0, 'ICF1': 5, 'TWD4': 4, 'CAL2': 2, 'PORTD4': 4, 'COM0B1': 5, 'ACI': 4, 'OCR3AL5': 5, 'OCIE2A': 1, 'ICR3L7': 7, 'WDP3': 5, 'OCF2A': 1, 'RCE': 3, 'RWAL': 5, 'TCNT3L2': 2, 'EORSMI': 5, 'OCDR5': 5, 'TXC1': 6, 'EERE': 0, 'SPI2X': 0, 'OCIE0A': 1, 'PCIF0': 0, 'USBE': 7, 'PORF': 0, 'DDB0': 0, 'ICR1L6': 6, 'OCR3BL7': 7, 'TCNT0_1': 1, 'OCR3CH4': 4, 'RSTCPU': 3, 'CPOL': 3, 'EEAR1': 1, 'INT2': 2, 'ADCH2': 2, 'OCR0A_5': 5, 'WGM22': 3, 'EORSTE': 3, 'TWAM6': 7, 'EPRST3': 3, 'UCPOL1': 0, 'UDR1_3': 3, 'OCR1CH2': 2, 'ADCH3': 3, 'TOV0': 0, 'OCR3BL2': 2, 'COM3A0': 6, 'UCSZ12': 2, 'UDR1_7': 7, 'MSTR': 4, 'SPEED': 3, 'TCNT2_2': 2, 'UMSEL11': 7, 'EEDR5': 5, 'COM2A1': 7, 'DDE6': 6, 'ADSC': 6, 'MPCM1': 0, 'TWA3': 4, 'OCR1CL1': 1, 'UCSZ10': 1, 'TWEA': 6, 'DDF4': 4, 'GPIOR21': 1, 'OCR1BH1': 1, 'PORTD6': 6, 'TWA0': 1, 'EEDR7': 7, 'OC4OE5': 5, 'ICR3H1': 1, 'PCINT7': 7, 'OCR3AH1': 1, 'TC43': 3, 'UADD5': 5, 'UPRSME': 6, 'CS22': 2, 'STALLRQ': 5, 'OC4OE3': 3, 'TCNT3H2': 2, 'DDF0': 0, 'SPDR0': 0, 'GPIOR10': 0, 'FOC1B': 6, 'SPDR3': 3, 'COM0B0': 4, 'OCR1BL7': 7, 'CS40': 0, 'OCR4A7': 7, 'GPIOR25': 5, 'ISC10': 2, 'USBS1': 3, 'TC41': 1, 'TCNT3L4': 4, 'ACBG': 6, 'PORTF4': 4, 'TCNT0_2': 2, 'ICR1L4': 4, 'ICR1H6': 6, 'PCINT4': 4}
        # avr._vect = {1: None, 2: None, 3: None, 4: None, 7: None, 9: None, 10: None, 11: None, 12: None, 16: None, 17: None, 18: None, 19: None, 20: None, 21: None, 22: None, 23: None, 24: None, 25: None, 26: None, 27: None, 28: None, 29: None, 30: None, 31: None, 32: None, 33: None, 34: None, 35: None, 36: None, 37: None, 38: None, 39: None, 40: None, 41: None, 42: None}
        # avr._vector_indices = {'TIMER3_COMPA_vect': 32, 'USART1_TX_vect': 27, 'WDT_vect': 12, 'PCINT0_vect': 9, 'USART1_UDRE_vect': 26, 'TIMER3_COMPC_vect': 34, 'USB_GEN_vect': 10, 'TIMER3_CAPT_vect': 31, 'TIMER1_OVF_vect': 20, 'TIMER0_OVF_vect': 23, 'USB_COM_vect': 11, 'TIMER0_COMPA_vect': 21, 'INT0_vect': 1, 'ADC_vect': 29, 'EE_READY_vect': 30, 'TIMER4_COMPD_vect': 40, 'TIMER1_COMPA_vect': 17, 'SPI_STC_vect': 24, 'ANALOG_COMP_vect': 28, 'TIMER3_OVF_vect': 35, 'INT2_vect': 3, 'INT3_vect': 4, 'TIMER4_FPF_vect': 42, 'TIMER1_COMPB_vect': 18, 'TIMER3_COMPB_vect': 33, 'TIMER1_CAPT_vect': 16, 'TIMER4_COMPB_vect': 39, 'TIMER4_COMPA_vect': 38, 'USART1_RX_vect': 25, 'INT6_vect': 7, 'INT1_vect': 2, 'TWI_vect': 36, 'TIMER4_OVF_vect': 41, 'TIMER1_COMPC_vect': 19, 'TIMER0_COMPB_vect': 22, 'SPM_READY_vect': 37}
        # avr._aliases = {}

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
