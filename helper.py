"""
Helper functions and classes.

@author Samuel Brian
"""

from struct import pack, unpack
import socket

def str_to_bytes(data):
    if data.__class__ == str:
        return bytes(data, "utf-8")

def bytes_to_str(data):
    if data.__class__ == bytes:
        return data.decode()

## Pack an integer number into a uint8 (1 byte string).
def uint8(num):
    return pack("<B", num)

## Pack an integer number into an int8 (1 byte string).
def int8(num):
    return pack("<b", num)

## Pack an integer number into a uint16 (2 byte string).
def uint16(num):
    return pack("<H", num)

## Pack an integer number into a int16 (2 byte string).
def int16(num):
    return pack("<h", num)

## Pack an integer number into a uint32 (4 byte string).
def uint32(num):
    return pack("<I", num)

## Pack an integer number into a int32 (4 byte string).
def int32(num):
    return pack("<i", num)

## Pack an integer number into a uint64 (8 byte string).
def uint64(num):
    return pack("<Q", num)

## Pack an integer number into a int64 (8 byte string).
def int64(num):
    return pack("<q", num)

## Pack a floating point number into a float32 (4 byte string).
def float32(num):
    return pack("<f", num)

## Unpack a uint8 (1 byte string) into an int.
def uint8R(num):
    return unpack("<B", num)[0]

## Unpack a int8 (1 byte string) into an int.
def int8R(num):
    return unpack("<b", num)[0]

## Unpack a uint16 (2 byte string) into an int.
def uint16R(num):
    return unpack("<H", num)[0]

## Unpack an int16 (2 byte string) into an int.
def int16R(num):
    return unpack("<h", num)[0]

## Unpack a uint32 (4 byte string) into an int.
def uint32R(num):
    return unpack("<I", num)[0]

## Unpack an int32 (4 byte string) into an int.
def int32R(num):
    return unpack("<i", num)[0]

## Unpack a uint64 (8 byte string) into an int.
def uint64R(num):
    return unpack("<Q", num)[0]

## Unpack an int64 (8 byte string) into an int.
def int64R(num):
    return unpack("<q", num)[0]

## Unpack a float32 (4 byte string) into a float.
def float32R(num):
    return unpack("<f", num)[0]


## Abstraction of socket client to file-like object for use with Piper
class SocketFile:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def read(self, num_bytes):
        # From Gordon McMillan's Socket Programming HOWTO
        data = b''
        while len(data) < num_bytes:
            chunk = self.sock.recv(num_bytes - len(data))
            if chunk == '': raise RuntimeError("Socket connection broken.")
            data = data + chunk
        return data

    def write(self, data):

        if data.__class__ == str:
            data = str_to_bytes(data)

        # From Gordon McMillan's Socket Programming HOWTO
        total_sent = 0
        while total_sent < len(data):
            sent = self.sock.send(data[total_sent:])
            if sent == 0: raise RuntimeError("Socket connection broken.")
            total_sent += sent

    def flush(self):
        #self.sock.flush()
        pass

    def close(self):
        self.sock.close()


## File-like object to join a SocketServer's read-file and write-file for use with Piper.
class RWFile:

    def __init__(self, rfile, wfile):
        self.rfile = rfile
        self.wfile = wfile

    def read(self, num_bytes):
        return self.rfile.read(num_bytes)

    def write(self, data):
        self.wfile.write(data)

    def flush(self):
        self.wfile.flush()

    def close(self):
        self.rfile.close()
        self.wfile.close()

