#/usr/bin/python3.10

import socket
import json

# self made socket wrapper lib for proj
# chat protocol, V3
# NOTE: ADDED PARAMETERS WILL BE ADDED INTO THE FRONT OF THE MESSAGE.
# THE ONLY THINGS THAT WILL GO IN THE HEADER ARE MESSAGE LENGTH AND VERSION.
# ADD IN PROPER DISCONNECT
# ADD IN CUSTOM PARAMETERS AS JSON AT THE BEGINNING

#disconnect message char
# CONSTANTS CONTROL PANEL
# MISC
DISCONNECT = chr(15525)
VERSION = 3
DEFAULT_PORT=12435
# SIZES
VERSION_SIZE = 8
MESSAGE_LENGTH_SIZE = 16 # length of message size indicator, in the header
CUSTOM_PARAMETER_LENGTH = 16 # like message_lenght_size, but with custom parameters.
HEADER_LEN = 64

class Client:
    """This can work in two different ways. One, pass the create_conn flag as
    False and pass in the socket as an argument. Other way is to create a socket
    that will connect to your desired port and host."""
    def __init__(self, host='localhost', port=DEFAULT_PORT):
        self.sock = socket.socket()
        self.sock.connect((host, port))
        self.custom_parameters = {}


    def send(self, msg:str):
        """First VERSION_SIZE of header is version
        The next MESSAGE_LENGTH_SIZE if the message length
        """
        version = int(VERSION).to_bytes(VERSION_SIZE, 'big')
        msglen = len(msg).to_bytes(MESSAGE_LENGTH_SIZE, 'big')
        custom_params = json.dumps(self.custom_parameters, indent=4).encode()
        custom_params_size = len(custom_params).to_bytes(CUSTOM_PARAMETER_LENGTH, 'big')
        # check things out
        header_content_size =  len(version + msglen + custom_params_size)
        # fill up whats left in the header with 0s
        # this should theoretically be the same number every time
        # but in case I change things in the future...
        filler = bytes((HEADER_LEN) - header_content_size)

        # all together now!!!!!!
        self.sock.send(version + msglen + custom_params_size +
        filler + custom_params + msg.encode())

    def recv(self):
        header = self.sock.recv(HEADER_LEN, socket.MSG_WAITALL)

        data_so_far = 0

        version = int.from_bytes(header[:VERSION_SIZE], 'big')
        data_so_far += VERSION_SIZE

        msglen = int.from_bytes(header[data_so_far:data_so_far + MESSAGE_LENGTH_SIZE ], 'big')
        data_so_far += MESSAGE_LENGTH_SIZE

        custom_params_length = int.from_bytes(header[data_so_far: data_so_far + CUSTOM_PARAMETER_LENGTH], 'big')
        custom_parameters = json.loads(self.sock.recv(custom_params_length, socket.MSG_WAITALL).decode())
        # ^ parse json and convert to a dictionary

        message = self.sock.recv(msglen, socket.MSG_WAITALL).decode()


        if version != VERSION:
            print("Version mismatch.")

        return message, custom_parameters

class Server(Client):
    """Same as client but it is intended to have *sock.accept() as
    its argument"""
    def __init__(self, connection, addr):
        self.sock = connection
        self.addr = addr
        self.custom_parameters = {}

def server_recv(sock):
    header = sock.recv(HEADER_LEN, socket.MSG_WAITALL)

    data_so_far = 0

    version = int.from_bytes(header[:VERSION_SIZE], 'big')
    data_so_far += VERSION_SIZE

    msglen = int.from_bytes(header[data_so_far:data_so_far + MESSAGE_LENGTH_SIZE ], 'big')
    data_so_far += MESSAGE_LENGTH_SIZE

    custom_params_length = int.from_bytes(header[data_so_far: data_so_far + CUSTOM_PARAMETER_LENGTH], 'big')
    custom_parameters = json.loads(sock.recv(custom_params_length, socket.MSG_WAITALL).decode())
    # ^ parse json and convert to a dictionary

    message = sock.recv(msglen, socket.MSG_WAITALL).decode()


    if version != VERSION:
        print("Version mismatch.")

    return message, custom_parameters

def server_send(sock, msg, custom_parameters):
    """First VERSION_SIZE of header is version
    The next MESSAGE_LENGTH_SIZE if the message length
    """
    version = int(VERSION).to_bytes(VERSION_SIZE, 'big')
    msglen = len(msg).to_bytes(MESSAGE_LENGTH_SIZE, 'big')
    custom_params = json.dumps(custom_parameters, indent=4).encode()
    custom_params_size = len(custom_params).to_bytes(CUSTOM_PARAMETER_LENGTH, 'big')
    # check things out
    header_content_size =  len(version + msglen + custom_params_size)
    # fill up whats left in the header with 0s
    # this should theoretically be the same number every time
    # but in case I change things in the future...
    filler = bytes((HEADER_LEN) - header_content_size)

    # all together now!!!!!!
    sock.send(version + msglen + custom_params_size +
    filler + custom_params + msg.encode())