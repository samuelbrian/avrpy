from leonardo import *

# The long initialisation
avr = AVR()
avr.parse("avrheaders/iom32u4.h")
avr.parse("avrheaders/portpins.h")
avr.connect()
leo = LeonardoBoard(avr)
ard = Arduino(leo)
avr.disconnect()

# The short initialisation
ard = Leonardo()
avr = ard.avr

# Turn the Leonardo's LED on (PC7, Arduino pin 13)
avr.DDRC  |= (1 << avr.DDD7)
avr.PORTC |= (1 << avr.PORTD7)

# Or use the equivalent Arduino code
ard.pinMode(13, OUTPUT)
ard.digitalWrite(13, HIGH)

# # Play with INT0 on PIND0
# avr.DDRD &= ~(1 << avr.DDD0)   # input
# avr.PORTD |= (1 << avr.PORTD0) # pullup
# avr.EICRA |= (1 << avr.ISC00)
# avr.EIMSK |= (1 << avr.INT0)
# avr.INT0_vect = print
# #avr.piper.start()


ard.pinMode(ard.board.A0, INPUT)
print(ard.analogRead(ard.board.A0))