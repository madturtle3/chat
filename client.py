import select
import socket
import sys
import os
sys.path.append(os.path.dirname(__file__))
import socklib

id_number = 0
username = ""
username_table = {} # for contact overrides

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", socklib.DEFAULT_PORT))
init_data = socklib.raw_recv(sock)
id_number = init_data["id"]
socklib.raw_send(sock, {"mode": "message", "id": -1, "message": "HELLO!"})

while True:
    reader, _, _ = select.select([sock, sys.stdin], [], [])
    for item in reader:
        if item == sock:
            data = socklib.raw_recv(sock)
            if data != socklib.DISCONNECT:
                if data["mode"] == "message":
                    if data["username"] == "":
                        data["username"] = data["id"]
                    print(f"[{data['username']}]: {data['message']}")
            else:
                print("server had bizarre thought patters")
                sock.close()
                exit(0)