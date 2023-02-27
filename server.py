import selectors
import socket
import sys
import os
sys.path.append(os.path.dirname(__file__))
import socklib

# create some variables
# username table is a table of usernames whose indexes correspond to the socket table
id_number = -1
sockets = []

# create server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", socklib.DEFAULT_PORT))
server.listen(5)

# create selector, data is a special tuple with all the information you will need
selector = selectors.DefaultSelector()
selector.register(server, selectors.EVENT_READ, {"socket": server, "id": id_number})
# server is id -1
# it is NOT registered in the socket array
id_number += 1

while True:
    for key, event in selector.select(0):
        if key.data["socket"] == server:
            new_sock, address = server.accept()
            selector.register(new_sock, selectors.EVENT_READ, {
                "socket": new_sock,
                "id": id_number
            })
            socklib.raw_send(new_sock, {"mode": "init", "id": id_number})
            sockets.append(new_sock)
            id_number += 1
        
        else:
            info = key.data
            sock = info["socket"]
            message = socklib.raw_recv(sock)
            if message == socklib.DISCONNECT:
                selector.unregister(sock)
            else:
                if message["mode"] == "message":
                    dest = message["id"]
                    if "useranme" in message.keys():
                        username = message["username"]
                    else:
                        username = ""
                    if dest == -1: # SEND TO ALL
                        print(message["message"])
                        for sock in sockets:
                            socklib.raw_send(sock, {"id": info["id"], "message": message["message"], "mode": "message", "username": username})
                    else:
                        socklib.raw_send(sockets[dest], {"id": info["id"], "message": message["message"], "mode": "message", "username": username})

