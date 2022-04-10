#/usr/bin/python3.10

import socket

# self made socket wrapper lib for proj
# chat protocol, V2
# CHANGES: remove username, fix version fixed bug in send function
# FUTURE NOTES: add custom parameters
# NOTE: ADDED PARAMETERS WILL BE ADDED INTO THE FRONT OF THE MESSAGE.
# THE ONLY THINGS THAT WILL GO IN THE HEADER ARE MESSAGE LENGTH AND VERSION.

#disconnect message char
# CONSTANTS CONTROL PANEL
# MISC
DISCONNECT = chr(4)
VERSION = 2
DEFAULT_PORT=12435
# SIZES
VERSION_SIZE = 8
MESSAGE_LENGTH_SIZE = 4 # length of message size indicator, in the header
HEADER_LEN = 64

class Client:
    def __init__(self, host='localhost', port=DEFAULT_PORT,
    create_conn=True, conn:socket.socket=None):
        """pass in ip and addr of destination"""
        if create_conn:
            self.sock = socket.socket()
            self.sock.connect((host, port))
        else:
            self.sock = conn
        # make sure username can fit in header


    def send(self, msg:str):
        """16 byte header, organized as follows 0 based:
        HEADER TABLE:
        len use [span] meaning
        ----------------------
        1 if disconnect
        12 bytes 1-5: Length of message
        """
        version = int(VERSION).to_bytes(VERSION_SIZE, 'big')
        msglen = len(msg).to_bytes(MESSAGE_LENGTH_SIZE, 'big')
        # check things out
        header_content_size =  len(version + msglen)
        # fill up whats left with an ETX ascii character and some 0s
        filler = bytes((HEADER_LEN) - header_content_size)

        # all together now!!!!!!
        self.sock.send(version + msglen + filler + msg.encode())

    def recv(self):
        header = self.sock.recv(HEADER_LEN, socket.MSG_WAITALL)
        version = chr(header[:VERSION_SIZE])

        if version != VERSION:
            print("Version mismatch.")

        msglen = int.from_bytes(header[VERSION_SIZE:MESSAGE_LENGTH_SIZE+VERSION_SIZE ], 'big')

        message = self.sock.recv(msglen, socket.MSG_WAITALL).decode()


        return message

def rawrecv(sock):
    header = sock.recv(HEADER_LEN, socket.MSG_WAITALL)
    version = chr(header[0])

    if version != VERSION:
        return "Version mismatch."

    msglen = int.from_bytes(header[1:5], 'big')

    message = sock.recv(msglen, socket.MSG_WAITALL).decode()

    return message