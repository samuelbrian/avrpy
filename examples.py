from leonardo import *

#### The long initialisation.
avr = AVR()
avr.parse("avrheaders/iom32u4.h")
avr.parse("avrheaders/portpins.h")
leo = LeonardoBoard(avr)
ard = Arduino(leo)
avr.connect()
# Do stuff here...
avr.disconnect()

#### The short initialisation.
ard = Leonardo()
ard.connect()

#### Read and write registers.
print(ard.OCR1A)
ard.TIMSK0 = 0x0F

#### Get a register "pointer" for passing around.
ptr = ard.ptr("DDRD")   # ptr = &DDRD;
ptr.set(0xF0)           # *ptr = 0xF0;
print(ptr.get())

##### Turn on the Leonardo's built-in LED (on PC7 a.k.a. Pin 13).
ard.DDRC  |= (1 << ard.DDD7)
ard.PORTC |= (1 << ard.PORTD7)

# Or use the equivalent Arduino code.
ard.pinMode(ard.LED_BUILTIN, OUTPUT)
ard.digitalWrite(ard.LED_BUILTIN, HIGH)

#### Read an ADC pin.
ard.pinMode(ard.A0, INPUT)
print(ard.analogRead(ard.A0))

#### Use interrupts.

# Write a function...
x = 0
busy = False
def cb():
    global x, busy
    if busy: return
    busy = True
    x += 10
    if x > 255: x = 0
    print("x=" + str(x))
    ard.analogWrite(ard.LED_BUILTIN, x)
    sleep(0.1)
    busy = False

# Attach it to INT0 (on PIND0)
ard.DDRD  &= invert(1 << ard.DDD0)    # Set as input. Use invert() rather than ~operator.
ard.PORTD |= (1 << ard.PORTD0)        # Set as pullup.
ard.EICRA |= (1 << ard.ISC60)         # Set interrupt condition.
ard.EIMSK |= (1 << ard.INT6)          # Enable interrupt.
ard.INT6_vect = cb                    # Attach the callback function to the ISR.

# Or do it the Arduino way - pin 7 is Interrupt 4 (INT0)
ard.pinMode(7, INPUT_PULLUP)
ard.attachInterrupt(4, cb, CHANGE)