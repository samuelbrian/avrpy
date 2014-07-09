__author__ = 'samuel'

def to_int(string):
    if "x" in string:
        return int(string, 16)
    else:
        return int(string, 10)

class AVRPy:

    def __init__(self, header_filename):
        self.parse(header_filename)

    ## Parse an AVR register header (e.g. iom32u4.h for the ATmega32U4).
    def parse(self, header_filename):

        self._frozen = False

        self._SFR_IO8 = {}      # IO8 register map
        self._SFR_IO16 = {}     # IO16 register map
        self._SFR_MEM8 = {}     # MEM8 register map
        self._SFR_MEM16 = {}    # MEM16 register map
        self.constants = {}     # other numerical constants
        self._vect = {}         # map vector names to callback functions
        self.vectorIndices = {} # map vector names to indices

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

        self._frozen = True



    def __setattr__(self, key, value):
        if hasattr(self, "_frozen") and self._frozen and not hasattr(self, key):
            raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__, key))
        object.__setattr__(self, key, value)

    # def __getattr__(self, item):
    #     if not hasattr(self, item):
    #          pass




avr = AVRPy("avrheaders/iom32u4.h")
