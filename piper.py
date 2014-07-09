"""
Piper - a simple multi-pipe communication protocol
Allows finite sized packets over multiple pipes in a single file-like read/write stream.

@author Samuel Brian
"""

from threading import Lock

from helper import *


PACKET_BEGIN    = 0xBE
PACKET_END      = 0xEF
MAX_PIPE_ID	    = 0xFF
MAX_DATA_LENGTH	= 0xFF

begin_byte  = PACKET_BEGIN.to_bytes(1, byteorder="big")
end_byte    = PACKET_END.to_bytes(1, byteorder="big")


class Piper():

    ## Construct a Piper.
    # @param file A file or file-like object that has read, write, flush, and close methods.
    # @param max_queue_len The maximum number of read packets to keep in memory for each pipe.
    def __init__(self, file, max_queue_len=100):
        self.file = file
        self.max_queue_len = max_queue_len

        # Number of discarded bytes to read before an exception is thrown
        self.max_discarded_bytes = 512

        # Synchronous
        self.read_queue = {}

        # Asynchronous
        self.async_callbacks = {}
        self.async_start = False

        # Thread locks
        self.read_lock = Lock()
        self.write_lock = Lock()

    ## Write a packet to a pipe.
    # @param pipe_id [int] The ID of the pipe to write the packet to.
    # @param data [string] The packet's payload data.
    # @throws Exception If the length of the data is greater than MAX_DATA_LENGTH or pipe_id is not between 0 and MAX_PIPE_ID.
    def write_packet(self, pipe_id, data):

        with self.write_lock:
            if data.__class__ == str:
                data = str_to_bytes(data)

            if len(data) > MAX_DATA_LENGTH:
                raise Exception("Data length ({0}) is greater than maximum of {1} bytes.".format(len(data), MAX_DATA_LENGTH))
            if pipe_id < 0 or pipe_id > MAX_PIPE_ID:
                raise Exception("Pipe ID ({0}) is not in valid range (between 0 and {1}.".format(pipe_id, MAX_PIPE_ID))
            packet = uint8(PACKET_BEGIN) + uint8(pipe_id) + uint8(len(data)) + data + uint8(PACKET_END)
            self.file.write(packet)
            self.file.flush()
            #print(packet)


    """ Asynchronous read API """

    ## Set the function to execute when a packet arrives with a particular pipe ID.
    # @param pipe_id The ID of the pipe endpoint.
    # @param callback_function A function that expects the payload data as first argument.
    def set_read_callback(self, pipe_id, callback_function):
        self.async_callbacks[pipe_id] = callback_function

    ## Start the Piper reading packets continuously and call callbacks set with set_read_callback().
    # If no callback is set for the pipe ID of a read packet, it is discarded.
    # This function blocks on reading from the file.
    def start(self):
        self.async_start = True
        # todo: mutex here
        while self.async_start:
            id, data = self.read_packet_from_file()
            if id in self.async_callbacks and self.async_callbacks[id] != None:
               self.async_callbacks[id](data)
            else:
                self.add_packet_to_queue(id, data)

    ## Stop the Piper reading continuously after the start() function is called.
    # For this to take effect, the start() loop must escape from the read call.
    def stop(self):
        # todo: mutex here
        self.async_start = False

    """ Synchronous read API """

    ## Get the next packet from a pipe.
    # Blocks until a packet arrives in the pipe, or returns immediately if already in the queue.
    # Adds any packets read with other pipe destinations to the queue, or calls its asynchronous callback function if
    # it is set. Queue maximum length removes oldest packets.
    # @param pipe_id [int] The number of the pipe to be read from.
    # @return [string|bytes] The packet's payload data.
    def read_packet(self, pipe_id):

        if pipe_id < 0 or pipe_id > MAX_PIPE_ID:
            raise Exception("Pipe ID ({0}) is not in valid range (between 0 and {1}.".format(pipe_id, MAX_PIPE_ID))

        # If a packet for this pipe is already in the queue, retrieve it now
        if pipe_id in self.read_queue and len(self.read_queue[pipe_id]) > 0:
            return self.read_queue[pipe_id].pop(0)

        # Read packets until one for this pipe
        while True:

            read_id, read_data = self.read_packet_from_file()

            if read_id == pipe_id:
                # Found a packet for this pipe, return the data
                return read_data
            elif read_id in self.async_callbacks and self.async_callbacks[read_id] != None:
                # Call the callback if there is one
                self.async_callbacks[read_id](read_data)
            else:
                # Otherwise add it to the queue
                self.add_packet_to_queue(read_id, read_data)

    """ Internal functions """

    ## Reads a packet from the file.
    # Blocks until a packet is read, the file ends or is closed, or max_discarded_bytes number of bytes are discarded.
    # @return (pipe_id, data) The pipe ID of the read packet and the byte data.
    def read_packet_from_file(self):

        pipe_id = None
        data = None
        discarded_bytes = 0

        while True:
            with self.read_lock:
                # Discard bytes until PACKET_BEGIN
                ch = self.read_byte()
                while ch != uint8(PACKET_BEGIN):
                    ch = self.read_byte()
                    discarded_bytes += 1
                    if discarded_bytes >= self.max_discarded_bytes:
                        raise Exception("Discarded {0} bytes. File probably isn't a Piper transmitter.".format(discarded_bytes))

                # Read pipe_id
                pipe_id = uint8R(self.read_byte())

                # Read data_length
                data_length = uint8R(self.read_byte())

                # Read data
                data = self.file.read(data_length)

                #print(data)

                if len(data) != data_length:
                    raise Exception("File closed.")

                if self.read_byte() != uint8(PACKET_END):
                    #print("Hey you! A packet is being discarded.")
                    discarded_bytes += len(data) + 2
                else:
                    break

        #print("read pipe {0}: {1}".format(pipe_id, data))
        return pipe_id, data

    def add_packet_to_queue(self, pipe_id, data):
        if pipe_id in self.read_queue:
            if len(self.read_queue[pipe_id]) >= self.max_queue_len:
                # Remove oldest if queue too long
                self.read_queue[pipe_id].pop(0)
            self.read_queue[pipe_id].append(data)
        else:
            self.read_queue[pipe_id] = [ data ]

    ## Read a single byte.
    def read_byte(self):
        ch = self.file.read(1)
        if len(ch) == 0:
            raise Exception("File closed.")
        return ch
