__author__ = 'samuel'

from serial import Serial
from serial.tools.list_ports import comports
from struct import pack, unpack
from piper import Piper
from helper import uint8, uint16, uint8R, uint16R

# Pipe addresses
REGISTER_PIPE   = 0x00
INTERRUPT_PIPE  = 0x01

# Operation tokens
READ8           = 0x01
READ16          = 0x02
WRITE8          = 0xF1
WRITE16         = 0xF2

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
                    self.vectorIndices[spl[1]] = to_int(matches.groups()[0])
                    self._vect[spl[1]] = None
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
            self.setValue(self._SFR_IO8[item], value, WRITE8)
        elif item in  object.__getattribute__(self, "_SFR_IO16"):
            self.setValue(self._SFR_IO16[item], value, WRITE16)
        elif item in  object.__getattribute__(self, "_SFR_MEM8"):
            self.setValue(self._SFR_MEM8[item], value, WRITE8)
        elif item in  object.__getattribute__(self, "_SFR_MEM16"):
            self.setValue(self._SFR_MEM16[item], value, WRITE16)
        elif item in  object.__getattribute__(self, "constants"):
            raise AttributeError("Constants are read-only attributes.")
        elif item in  object.__getattribute__(self, "_vect"):
            if not (callable(value) or None):
                raise AttributeError("Interrupt vectors must be assigned a callable object or None.")
            self._vect[item] = value
        else:
            object.__setattr__(self, item, value)

    def __getattr__(self, item):

        if item in object.__getattribute__(self, "_SFR_IO8"):
            return self.getValue(self._SFR_IO8[item], READ8)
        if item in object.__getattribute__(self, "_SFR_IO16"):
            return self.getValue(self._SFR_IO16[item], READ16)
        if item in object.__getattribute__(self, "_SFR_MEM8"):
            return self.getValue(self._SFR_MEM8[item], READ8)
        if item in object.__getattribute__(self, "_SFR_MEM16"):
            return self.getValue(self._SFR_MEM16[item], READ16)
        if item in object.__getattribute__(self, "constants"):
            return self.constants[item]
        if item in object.__getattribute__(self, "_vect"):
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
                    or item in object.__getattribute__(self, "_vect")       \
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
        if write_token == WRITE8:    packet += uint8(value)
        elif write_token == WRITE16: packet += uint16(value)
        self.piper.write_packet(REGISTER_PIPE, packet)


# Testing...
avr = AVRPy()
avr.parse("avrheaders/iom32u4.h")
avr.connect()
