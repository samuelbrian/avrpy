"""
@author Samuel Brian
"""

from serial import Serial
from serial.tools.list_ports import comports
from piper import Piper
from helper import uint8, uint16, uint8R, uint16R, to_int

def _BV(bit): return 1 << bit
# Bitwise invert because Python's ~ is signed two's complement
def invert(num): return ~num & 0xFFFF
def invert8(num): return ~num & 0xFF

class AVRPy:

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

    def __init__(self, port=0):
        self._frozen = False    # flag to allow/disallow setting attributes
        self._SFR_IO8 = {}      # IO8 register map
        self._SFR_IO16 = {}     # IO16 register map
        self._SFR_MEM8 = {}     # MEM8 register map
        self._SFR_MEM16 = {}    # MEM16 register map
        self._constants = {}     # other numerical constants
        self._vect = {}         # map vector names to callback functions
        self._vector_indices = {} # map vector names to indices
        self._int_enabled = True
        self._aliases = {}
        self._serial = None
        self._piper = None
        self._frozen = True

    def connect(self, port=0, baudrate=38400):
        if port.__class__ == int:
            # Port is an integer. Use as index into port list.
            ports = self.list_ports()
            if len(ports) < port or len(ports) == 0:
                raise Exception("Port index out of range - no serial port available to connect to AVR.")
            port = ports[port][0]

        try:
            self._serial = Serial(port, baudrate)
            self._piper = Piper(self._serial)
            self._piper.set_read_callback(AVRPy.INTERRUPT_PIPE, self._handleInterrupt)
        except Exception as e:
            raise Exception("Could not connect to AVR on serial port {0}.".format(port))

    def list_ports(self):
        return list(comports())

    def disconnect(self):
        self._serial.close()

    ## Parse an AVR register header (e.g. iom32u4.h for the ATmega32U4).
    def parse(self, header_filename):
        import re
        with open(header_filename, "r") as file:
            for line in file:

                #if not line.startswith("#define "): continue
                matches = re.search("#\s*define\s+", line)
                if matches is None: continue
                spl = line.replace(matches.group(0), "")
                same = False
                while same:
                    pspl = spl
                    spl = spl.replace("  ", " ")
                    same = pspl == spl
                spl = spl.strip().split(" ")

                # Constants with no value
                if len(spl) < 2:
                    self._constants[spl[0]] = None
                    continue

                # IO8 registers
                matches = re.search("_SFR_IO8\((.+)\)", spl[1])
                if matches is not None:
                    self._SFR_IO8[spl[0]] = to_int(matches.groups()[0])
                    continue

                # IO16 registers
                matches = re.search("_SFR_IO16\((.+)\)", spl[1])
                if matches is not None:
                    self._SFR_IO16[spl[0]] = to_int(matches.groups()[0])
                    continue

                # MEM8 registers
                matches = re.search("_SFR_MEM8\((.+)\)", spl[1])
                if matches is not None:
                    self._SFR_MEM8[spl[0]] = to_int(matches.groups()[0])
                    continue

                # MEM16 registers
                matches = re.search("_SFR_MEM16\((.+)\)", spl[1])
                if matches is not None:
                    self._SFR_MEM16[spl[0]] = to_int(matches.groups()[0])
                    continue

                # Interrupt vectors
                matches = re.search("_VECTOR\((.+)\)", line)
                if matches is not None:
                    index = to_int(matches.groups()[0])
                    self._vector_indices[spl[0]] = index
                    self._vect[index] = None
                    continue

                # Other constants
                try:
                    self._constants[spl[0]] = to_int(spl[1])
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
            self._set_value(self._SFR_IO8[item], value, AVRPy.WRITE_IO8)
        elif item in object.__getattribute__(self, "_SFR_IO16"):
            self._set_value(self._SFR_IO16[item], value, AVRPy.WRITE_IO16)
        elif item in object.__getattribute__(self, "_SFR_MEM8"):
            self._set_value(self._SFR_MEM8[item], value, AVRPy.WRITE_MEM8)
        elif item in object.__getattribute__(self, "_SFR_MEM16"):
            self._set_value(self._SFR_MEM16[item], value, AVRPy.WRITE_MEM16)
        elif item in object.__getattribute__(self, "_aliases"):
            self._set_value(self._aliases[item][0], value, self._aliases[item][2])
        elif item in object.__getattribute__(self, "_constants"):
            raise AttributeError("Constants are read-only attributes.")
        elif item in object.__getattribute__(self, "_vector_indices"):
            index = self._vector_indices[item]
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
            return self._get_value(self._SFR_IO8[item], AVRPy.READ_IO8)
        if item in object.__getattribute__(self, "_SFR_IO16"):
            return self._get_value(self._SFR_IO16[item], AVRPy.READ_IO16)
        if item in object.__getattribute__(self, "_SFR_MEM8"):
            return self._get_value(self._SFR_MEM8[item], AVRPy.READ_MEM8)
        if item in object.__getattribute__(self, "_SFR_MEM16"):
            return self._get_value(self._SFR_MEM16[item], AVRPy.READ_MEM16)
        if item in object.__getattribute__(self, "_aliases"):
            return self._get_value(self._aliases[item][0], self._aliases[item][1])
        if item in object.__getattribute__(self, "_constants"):
            return self._constants[item]
        if item in object.__getattribute__(self, "_vector_indices"):
            raise AttributeError("Interrupt vectors are write-only attributes.")
        else:
            return object.__getattribute__(self, item)

    def __hasattr__(self, item):
        # The built-in hasattr() checks if getattr() throws an exception or not. This will cause unnecessary serial
        # communication. This overridden hasattr() does not do this.
        try:
            return self.defined(item) or item in object.__getattribute__(self, "vectorIndices") or item in self.__dict__
        except:
            return item in self.__dict__

    def _get_value(self, address, read_token):
        self._piper.write_packet(AVRPy.REGISTER_PIPE, uint8(address) + uint8(read_token))
        value = self._piper.read_packet(AVRPy.REGISTER_PIPE)
        if len(value) == 2:   return uint16R(value)
        elif len(value) == 1: return uint8R(value)
        return -1

    def _set_value(self, address, value, write_token):
        packet = uint8(address) + uint8(write_token)
        if write_token == AVRPy.WRITE_IO8 or write_token == AVRPy.WRITE_MEM8: packet += uint8(value)
        elif write_token == AVRPy.WRITE_IO16 or write_token == AVRPy.WRITE_MEM16: packet += uint16(value)
        self._piper.write_packet(AVRPy.REGISTER_PIPE, packet)

    def define(self, name, value):
        if value in object.__getattribute__(self, "_SFR_IO8"):
            self._aliases[name] = (self._SFR_IO8[value], AVRPy.READ_IO8, AVRPy.WRITE_IO8)
        elif value in object.__getattribute__(self, "_SFR_IO16"):
            self._aliases[name] = (self._SFR_IO16[value], AVRPy.READ_IO16, AVRPy.WRITE_IO16)
        elif value in object.__getattribute__(self, "_SFR_MEM8"):
            self._aliases[name] = (self._SFR_MEM8[value], AVRPy.READ_MEM8, AVRPy.WRITE_MEM8)
        elif value in object.__getattribute__(self, "_SFR_MEM16"):
            self._aliases[name] = (self._SFR_MEM16[value], AVRPy.READ_MEM16, AVRPy.WRITE_MEM16)
        else:
            self._constants[name] = value

    def undef(self, name):
        try: del self._constants[name]
        except: pass
        try: del self._aliases[name]
        except: pass

    def defined(self, item):
        return self.is_register(item) or self.is_constant(item)

    def is_register(self, name):
        return name in object.__getattribute__(self, "_SFR_IO8") \
                    or name in object.__getattribute__(self, "_SFR_IO16") \
                    or name in object.__getattribute__(self, "_SFR_MEM8") \
                    or name in object.__getattribute__(self, "_SFR_MEM16") \
                    or name in object.__getattribute__(self, "_aliases")

    def is_constant(self, name):
        return name in object.__getattribute__(self, "_constants")

    def is_vect(self, name):
        return name in object.__getattribute__(self, "_vect")

    # Enable global interrupts. Handles incoming interrupt packets. Doesn't actually change AVR's SREG.
    def sei(self):
        self._int_enabled = True

    # Disable global interrupts. Ignores incoming interrupt packets. Doesn't actually change AVR's SREG.
    def cli(self):
        self._int_enabled = False

    # Useful but obsolete macros from http://www.nongnu.org/avr-libc/user-manual/group__deprecated__items.html
    ## Set bit.
    def sbi(self, sfr, bit):
        self.__setattr__(sfr, self.__getattr__(sfr) | (1 << bit))

    ## Clear bit.
    def cbi(self, sfr, bit):
        self.__setattr__(sfr, self.__getattr__(sfr) & invert(1 << bit))

    def bit_is_set(self, sfr, bit):
        return bool(self.__getattr__(sfr) & (1 << bit))

    def bit_is_clear(self, sfr, bit):
        return not self.bit_is_set(sfr, bit)

    def ptr(self, register_name):
        return Register(self, register_name)

    ## Enable the interrupt packet being generated on the microcontroller.
    def enableInterrupt(self, index):
        if isinstance(index, str): index = self._vector_indices[index]
        self._piper.write_packet(AVRPy.INTERRUPT_PIPE, uint8(index) + uint8(AVRPy.INT_ENABLE))

    ## Disable the interrupt packet being generated on the microcontroller.
    def disableInterrupt(self, index):
        if isinstance(index, str): index = self._vector_indices[index]
        self._piper.write_packet(AVRPy.INTERRUPT_PIPE, uint8(index) + uint8(AVRPy.INT_DISABLE))

    def _handleInterrupt(self, index):
        if not self._int_enabled: return
        index = uint8R(index)
        if self._vect[index] is not None: self._vect[index](index)

    def generateFirmwareISRs(self):
        s = ""
        for interrupt_name in sorted(self._vector_indices, key=self._vector_indices.get):
            s += "ISR({0}) {{ triggerInterrupt({1}); }}\n".format(interrupt_name, avr._vector_indices[interrupt_name])
        return s


class Register:

    def __init__(self, avr, register_name):
        self.avr = avr
        self.register = register_name

    def set(self, value):
        self.avr.__setattr__(self.register, value)

    def get(self):
        return self.avr.__setattr__(self.register)


# To allow built-in hasattr() to be overridden. See AVRPy.__hasattr__() for an explanation.
# From http://code.activestate.com/lists/python-list/14972/
def hasattr(o, a, orig_hasattr=hasattr):
    if orig_hasattr(o, "__hasattr__"):
        return o.__hasattr__(a)
    return orig_hasattr(o, a)
__builtins__.hasattr = hasattr


# # Testing...
# avr = AVRPy()
# avr.parse("avrheaders/iom32u4.h")
# avr.parse("avrheaders/portpins.h")
# avr.connect()
#
# # Play with INT0 on PIND0
# avr.DDRD &= ~(1 << avr.DDD0)
# avr.PORTD |= (1 << avr.PORTD0)
# avr.EICRA |= (1 << avr.ISC00)
# avr.EIMSK |= (1 << avr.INT0)
# avr.INT0_vect = print
# #avr.piper.start()

