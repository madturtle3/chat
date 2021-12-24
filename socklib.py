import socket
import random

# self made socket wrapper lib for proj
# chat protocol, V1
#disconnect message char
DISCONNECT = chr(4)
VERSION = 1
HEADER_LEN=16
PORT=12435
class Client:
    def __init__(self, host='localhost', port=12435,
    username:str=f"Guest#{random.randint(1,PORT)}",
    create_conn=True, conn:socket.socket=None):
        """pass in ip and addr of destination"""
        if create_conn:
            self.sock = socket.socket()
            self.sock.connect((host, port))
        else:
            self.sock = conn
        # make sure username can fit in header
        self.username = username[:15]

    def send(self, msg:str):
        """16 byte header, organized as follows 0 based:
        len use [ span] meaning
        1 if disconnect
        4 bytes 1-5: Length of message
        16 username 5-16"""
        version = int(1).to_bytes(1, 'big')
        msglen = len(msg).to_bytes(4, 'big')
        # check things out
        headerlen =  len(version + msglen + self.username.encode())
        # fill up whats left with an ETX ascii character and some 0s
        filler = bytes((HEADER_LEN) - headerlen)

        # all together now!!!!!!
        self.sock.send(version + msglen + self.username.encode() + filler + msg.encode())

    def recv(self):
        header = self.sock.recv(HEADER_LEN, socket.MSG_WAITALL)
        version = chr(header[0])

        msglen = int.from_bytes(header[1:5], 'big')
        username = header[5:].decode().replace('\x00',"").replace('\x03', "")

        message = self.sock.recv(msglen, socket.MSG_WAITALL).decode()


        return username, message

def rawrecv(sock):
    header = sock.recv(HEADER_LEN, socket.MSG_WAITALL)
    version = chr(header[0])

    msglen = int.from_bytes(header[1:5], 'big')
    username = header[5:].decode().replace('\x00',"").replace('\x03', "")

    message = sock.recv(msglen, socket.MSG_WAITALL).decode()

    return username, message