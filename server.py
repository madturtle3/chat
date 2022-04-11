from socklib import *
import socket
import select

inputs = []
outputs = []
connections = {}

def sendtoall(message:str):
    for connection in connections.values():
        connection.send(message)


def main():
    try:
        sock = socket.socket()
        sock.bind(("", PORT))
        sock.listen(5)
        inputs.append(sock)
    except Exception as err:
        sock.close()
        raise err
    running = True
    while running:
        read_buffers, write_buffers, errors = select.select(inputs, outputs, inputs)

        for fd in read_buffers:
            if fd == sock:
                conn, addr = sock.accept()
                new_client = Client(create_conn=False, conn=conn, username='server') # create client for sending later
                username, _ = new_client.recv() # empty message to get username
                connections[username] = new_client
                inputs.append(conn) # add to select list
            else:
                username, new_msg = rawrecv(fd)
                print(new_msg)
                if new_msg != DISCONNECT: # if message is not empty bytes
                    sendtoall(f"{username}: {new_msg}") # relay message to all other people

                else: # disconnect sent, close connection
                    inputs.pop(inputs.index(fd))
                    connections.pop(username)
                    
            

if __name__ == "__main__":
    main()