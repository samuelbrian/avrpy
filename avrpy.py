"""
@author Samuel Brian
"""

from serial import Serial
from serial.tools.list_ports import comports
from struct import pack, unpack
from piper import Piper
from helper import uint8, uint16, uint8R, uint16R

# Pipe addresses
REGISTER_PIPE   = 0x00
INTERRUPT_PIPE  = 0x01

# Operation tokens
READ_IO8        = 0x01
READ_IO16       = 0x02
READ_MEM8       = 0x03
READ_MEM16      = 0x04
WRITE_IO8       = 0xF1
WRITE_IO16      = 0xF2
WRITE_MEM8      = 0xF3
WRITE_MEM16     = 0xF4
INT_ENABLE      = 0x01
INT_DISABLE     = 0x00

def to_int(string):
    return int(string, 16) if "x" in string else int(string, 10)

# To allow built-in hasattr() to be overridden. See AVRPy.__hasattr__() for an explanation.
# From http://code.activestate.com/lists/python-list/14972/
def hasattr(o, a, orig_hasattr=hasattr):
    if orig_hasattr(o, "__hasattr__"):
        return o.__hasattr__(a)
    return orig_hasattr(o, a)
__builtins__.hasattr = hasattr


class AVRPy:

    def __init__(self, port=0):
        self._frozen = False    # flag to allow/disallow setting attributes
        self._SFR_IO8 = {}      # IO8 register map
        self._SFR_IO16 = {}     # IO16 register map
        self._SFR_MEM8 = {}     # MEM8 register map
        self._SFR_MEM16 = {}    # MEM16 register map
        self.constants = {}     # other numerical constants
        self._vect = {}         # map vector names to callback functions
        self.vectorIndices = {} # map vector names to indices
        self.serial = None
        self.piper = None
        self._frozen = True

    def connect(self, port=0, baudrate=38400):
        if port.__class__ == int:
            # Port is an integer. Use as index into port list.
            ports = self.list_ports()
            if len(ports) < port or len(ports) == 0:
                raise Exception("Port index out of range - no serial port available to connect to AVR.")
            port = ports[port][0]

        try:
            self.serial = Serial(port, baudrate)
            self.piper = Piper(self.serial)
            self.piper.set_read_callback(INTERRUPT_PIPE, self.handleInterrupt)
        except Exception as e:
            raise Exception("Could not connect to AVR on serial port {0}.".format(port))

    def list_ports(self):
        return list(comports())

    def disconnect(self):
        self.serial.close()

    ## Parse an AVR register header (e.g. iom32u4.h for the ATmega32U4).
    def parse(self, header_filename):

        import re
        with open(header_filename, "r") as file:
            for line in file:
                if not line.startswith("#define "): continue
                spl = line.strip().split(" ")

                # Constants with no value
                if len(spl) < 3:
                    self.constants[spl[1]] = None
                    continue

                # IO8 registers
                matches = re.search("_SFR_IO8\((.+)\)", spl[2])
                if matches is not None:
                    self._SFR_IO8[spl[1]] = to_int(matches.groups()[0])
                    continue

                # IO16 registers
                matches = re.search("_SFR_IO16\((.+)\)", spl[2])
                if matches is not None:
                    self._SFR_IO16[spl[1]] = to_int(matches.groups()[0])
                    continue

                # MEM8 registers
                matches = re.search("_SFR_MEM8\((.+)\)", spl[2])
                if matches is not None:
                    self._SFR_MEM8[spl[1]] = to_int(matches.groups()[0])
                    continue

                # MEM16 registers
                matches = re.search("_SFR_MEM16\((.+)\)", spl[2])
                if matches is not None:
                    self._SFR_MEM16[spl[1]] = to_int(matches.groups()[0])
                    continue

                # Interrupt vectors
                matches = re.search("_VECTOR\((.+)\)", line)
                if matches is not None:
                    index = to_int(matches.groups()[0])
                    self.vectorIndices[spl[1]] = index
                    self._vect[index] = None
                    continue

                # Other constants
                try:
                    self.constants[spl[1]] = to_int(spl[2])
                    continue
                except:
                    pass

                # Unhandled: FUSE_*, RAM*, XRAM*, _VECTOR_SIZE, and some others.
                #print(line)

    def __setattr__(self, item, value):
        if hasattr(self, "_frozen") and self._frozen and not hasattr(self, item):
            raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__, item))
        if not hasattr(self, "_frozen") or (hasattr(self, "_frozen") and not self._frozen):
            object.__setattr__(self, item, value)
            return

        if item in object.__getattribute__(self, "_SFR_IO8"):
            self.setValue(self._SFR_IO8[item], value, WRITE_IO8)
        elif item in  object.__getattribute__(self, "_SFR_IO16"):
            self.setValue(self._SFR_IO16[item], value, WRITE_IO16)
        elif item in  object.__getattribute__(self, "_SFR_MEM8"):
            self.setValue(self._SFR_MEM8[item], value, WRITE_MEM8)
        elif item in  object.__getattribute__(self, "_SFR_MEM16"):
            self.setValue(self._SFR_MEM16[item], value, WRITE_MEM16)
        elif item in  object.__getattribute__(self, "constants"):
            raise AttributeError("Constants are read-only attributes.")
        elif item in  object.__getattribute__(self, "vectorIndices"):
            index = self.vectorIndices[item]
            if callable(value):
                self._vect[index] = value
                self.enableInterrupt(index)
            elif value is None:
                self._vect[index] = None
                self.disableInterrupt(index)
            else:
                raise AttributeError("Interrupt vectors must be assigned a callable object or None.")

        else:
            object.__setattr__(self, item, value)

    def __getattr__(self, item):

        if item in object.__getattribute__(self, "_SFR_IO8"):
            return self.getValue(self._SFR_IO8[item], READ_IO8)
        if item in object.__getattribute__(self, "_SFR_IO16"):
            return self.getValue(self._SFR_IO16[item], READ_IO16)
        if item in object.__getattribute__(self, "_SFR_MEM8"):
            return self.getValue(self._SFR_MEM8[item], READ_MEM8)
        if item in object.__getattribute__(self, "_SFR_MEM16"):
            return self.getValue(self._SFR_MEM16[item], READ_MEM16)
        if item in object.__getattribute__(self, "constants"):
            return self.constants[item]
        if item in object.__getattribute__(self, "vectorIndices"):
            raise AttributeError("Interrupt vectors are write-only attributes.")
        else:
            return object.__getattribute__(self, item)

    def __hasattr__(self, item):
        # The built-in hasattr() checks if getattr() throws an exception or not. This will cause unnecessary serial
        # communication. This overridden hasattr() does not do this.
        try:
            return item in object.__getattribute__(self, "_SFR_IO8")        \
                    or item in object.__getattribute__(self, "_SFR_IO16")   \
                    or item in object.__getattribute__(self, "_SFR_MEM8")   \
                    or item in object.__getattribute__(self, "_SFR_MEM16")  \
                    or item in object.__getattribute__(self, "constants")   \
                    or item in object.__getattribute__(self, "vectorIndices")       \
                    or item in self.__dict__
        except:
            return item in self.__dict__

    def getValue(self, address, read_token):
        self.piper.write_packet(REGISTER_PIPE, uint8(address) + uint8(read_token))
        value = self.piper.read_packet(REGISTER_PIPE)
        if len(value) == 2:   return uint16R(value)
        elif len(value) == 1: return uint8R(value)
        return -1

    def setValue(self, address, value, write_token):
        packet = uint8(address) + uint8(write_token)
        if write_token == WRITE_IO8 or write_token == WRITE_MEM8: packet += uint8(value)
        elif write_token == WRITE_IO16 or write_token == WRITE_MEM16: packet += uint16(value)
        self.piper.write_packet(REGISTER_PIPE, packet)

    def handleInterrupt(self, index):
        index = uint8R(index)
        print("Interrupt " + str(index))
        if self._vect[index] is not None: self._vect[index](index)

    def enableInterrupt(self, index):
        self.piper.write_packet(INTERRUPT_PIPE, uint8(index) + uint8(INT_ENABLE))

    def disableInterrupt(self, index):
        self.piper.write_packet(INTERRUPT_PIPE, uint8(index) + uint8(INT_DISABLE))

    def generateFirmwareISRs(self):
        s = ""
        for interrupt_name in sorted(self.vectorIndices, key=self.vectorIndices.get):
            s += "ISR({0}) {{ triggerInterrupt({1}); }}\n".format(interrupt_name, avr.vectorIndices[interrupt_name])
        return s


# # Testing...
# avr = AVRPy()
# avr.parse("avrheaders/iom32u4.h")
# avr.connect()
#
# # Play with INT0 on PIND0
# avr.DDRD &= ~(1 << avr.DDD0)
# avr.PORTD |= (1 << avr.PORTD0)
# avr.EICRA |= (1 << avr.ISC00)
# avr.EIMSK |= (1 << avr.INT0)
# avr.INT0_vect = print
# avr.piper.start()
