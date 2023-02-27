#/usr/bin/python3.10

import socket
import json

# self made socket wrapper lib for proj
# chat protocol, V3

# CONSTANTS CONTROL PANEL
# MISC
DISCONNECT = -1
VERSION = 4
DEFAULT_PORT=12435
# SIZES
VERSION_SIZE = 8
MESSAGE_LENGTH = 16 # length of message size definition in header
HEADER_LEN = 64

def recv(sock):
    header = sock.recv(HEADER_LEN, socket.MSG_WAITALL)
    if not header:
        return DISCONNECT, {}
    data_so_far = 0

    version = int.from_bytes(header[:VERSION_SIZE], 'big')
    data_so_far += VERSION_SIZE

    message_length = int.from_bytes(header[data_so_far: data_so_far + MESSAGE_LENGTH], 'big')
    message = json.loads(sock.recv(message_length, socket.MSG_WAITALL).decode())
    # ^ parse json and convert to a dictionary




    if version != VERSION:
        print("Version mismatch.")

    return message

def send(sock, message):
    """First VERSION_SIZE of header is version
    The next MESSAGE_LENGTH_SIZE is the message length
    """
    version = int(VERSION).to_bytes(VERSION_SIZE, 'big')
    custom_params = json.dumps(message, indent=4).encode()
    custom_params_size = len(custom_params).to_bytes(MESSAGE_LENGTH, 'big')
    # check things out
    header_content_size =  len(version + custom_params_size)
    # fill up whats left in the header with 0s
    # this should theoretically be the same number every time
    # but in case I change things in the future...
    filler = bytes((HEADER_LEN) - header_content_size)

    # all together now!!!!!!
    sock.send(version + custom_params_size +
    filler + custom_params)
