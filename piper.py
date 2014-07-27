"""
Piper - a simple multi-pipe communication protocol
Allows finite sized packets over multiple pipes in a single file-like read/write stream.

@author Samuel Brian
"""

from threading import Lock, Thread
from struct import pack, unpack
from time import sleep

class Piper():

    PACKET_BEGIN    = 0xBE
    PACKET_END      = 0xEF
    MAX_PIPE_ID	    = 0xFF
    MAX_DATA_LENGTH	= 0xFF

    ## Construct a Piper.
    # @param file A file or file-like object that has read, write, flush, and close methods.
    # @param max_queue_len The maximum number of read packets to keep in memory for each pipe.
    def __init__(self, file, max_queue_len=100):
        self.file = file
        self.max_queue_len = max_queue_len

        # Number of discarded bytes to read before an exception is thrown
        self.max_discarded_bytes = 512
        self.begin_byte  = Piper.PACKET_BEGIN.to_bytes(1, byteorder="big")
        self.end_byte    = Piper.PACKET_END.to_bytes(1, byteorder="big")

        # Synchronous
        self.read_queue = {}

        # Asynchronous
        self.async_callbacks = {}
        self.async_start = False

        # Thread locks
        self.write_lock = Lock()

        # Start read thread
        Thread(target=self._read_thread).start()

    ## Close the file and stop the read thread.
    def close(self):
        self.async_start = False
        if self.file is not None:
            self.file.close()

    ## Write a packet to a pipe.
    # @param pipe_id [int] The ID of the pipe to write the packet to.
    # @param data [string] The packet's payload data.
    # @throws Exception If the length of the data is greater than MAX_DATA_LENGTH or pipe_id is not between 0 and MAX_PIPE_ID.
    def write_packet(self, pipe_id, data):
        with self.write_lock:
            if data.__class__ == str:
                data = bytes(data, "utf-8")

            if len(data) > Piper.MAX_DATA_LENGTH:
                raise Exception("Data length ({0}) is greater than maximum of {1} bytes.".format(len(data), Piper.MAX_DATA_LENGTH))
            if pipe_id < 0 or pipe_id > Piper.MAX_PIPE_ID:
                raise Exception("Pipe ID ({0}) is not in valid range (between 0 and {1}.".format(pipe_id, Piper.MAX_PIPE_ID))
            packet = uint8(Piper.PACKET_BEGIN) + uint8(pipe_id) + uint8(len(data)) + data + uint8(Piper.PACKET_END)
            self.file.write(packet)
            self.file.flush()

    ## Set the function to execute when a packet arrives with a particular pipe ID.
    # @param pipe_id The ID of the pipe endpoint.
    # @param callback_function A function that expects the payload data as first argument.
    def set_read_callback(self, pipe_id, callback_function):
        self.async_callbacks[pipe_id] = callback_function

    ## Get the next packet from a pipe.
    # Blocks until a packet arrives in the pipe, or returns immediately if already in the queue.
    # The queue won't be filled if a read callback is set for the pipe.
    # @param pipe_id [int] The number of the pipe to be read from.
    # @return [string|bytes] The packet's payload data.
    def read_packet(self, pipe_id):
        if pipe_id < 0 or pipe_id > Piper.MAX_PIPE_ID:
            raise Exception("Pipe ID ({0}) is not in valid range (between 0 and {1}.".format(pipe_id, Piper.MAX_PIPE_ID))
        while not (pipe_id in self.read_queue and len(self.read_queue[pipe_id]) > 0):
            sleep(0)
        return self.read_queue[pipe_id].pop(0)

    """ Private functions """

    ## Reads a packet from the file.
    # Blocks until a packet is read, the file ends or is closed, or max_discarded_bytes number of bytes are discarded.
    # @return (pipe_id, data) The pipe ID of the read packet and the byte data.
    def _read_packet_from_file(self):
        pipe_id = None
        data = None
        discarded_bytes = 0

        while True:
            # Discard bytes until PACKET_BEGIN
            ch = self._read_byte()
            while ch != uint8(Piper.PACKET_BEGIN):
                discarded_bytes += 1
                print("Discarding one byte waiting for PACKET_BEGIN. {0} bytes so far.".format(discarded_bytes)) ### :(
                if discarded_bytes >= self.max_discarded_bytes:
                    raise Exception("Discarded {0} bytes. File probably isn't a Piper transmitter.".format(discarded_bytes))
                ch = self._read_byte()

            # Read pipe_id
            pipe_id = uint8R(self._read_byte())

            # Read data_length
            data_length = uint8R(self._read_byte())

            # Read data
            #data = self.file.read(data_length)
            data = b''
            while len(data) < data_length:
                data += self._read_byte()

            ch = self._read_byte()
            if ch != uint8(Piper.PACKET_END):
                discarded_bytes += len(data) + 2
                print("Packet discarded while expecting PACKET_END. {0} bytes so far.".format(discarded_bytes)) ### :(
            else:
                break

        return pipe_id, data

    ## Private read processing function. Called by start().
    def _read_thread(self):
        self.async_start = True
        try:
            while self.async_start:
                id, data = self._read_packet_from_file()
                if id in self.async_callbacks and self.async_callbacks[id] is not None:
                    Thread(target=self.async_callbacks[id], args=(data,)).start()
                else:
                    self._add_packet_to_queue(id, data)
        except Exception as e:
            if self.async_start: # Exception is expected when close() closes the file during a read, else reraise
                raise e

    # Add a read packet to the read queue for reading by read_packet()
    def _add_packet_to_queue(self, pipe_id, data):
        if pipe_id in self.read_queue:
            if len(self.read_queue[pipe_id]) >= self.max_queue_len:
                # Remove oldest if queue too long
                self.read_queue[pipe_id].pop(0)
            self.read_queue[pipe_id].append(data)
        else:
            self.read_queue[pipe_id] = [ data ]

    ## Read a single byte.
    def _read_byte(self):
        ch = self.file.read(1)
        if len(ch) == 0:
            raise Exception("File closed.")
        return ch

## Pack an integer number into a uint8 (1 byte string).
def uint8(num):
    num = max(min(num, 0xFF), 0x00)
    return pack("<B", num)

## Unpack a uint8 (1 byte string) into an int.
def uint8R(num):
    return unpack("<B", num)[0]
