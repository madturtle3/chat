import socket
from chat.socklib1 import DISCONNECT
import socklib
import select

poll = select.poll()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("localhost", socklib.DEFAULT_PORT))
server.listen(5)

poll.register(server, select.POLLIN)

username_table = {}

running = True
while running:
    try:
        for fd, type in poll.poll():
            if fd == server.fileno():
                new_conn, ip = server.accept()
                poll.register(new_conn)
                _, info = socklib.raw_recv(new_conn)
                username_table[info["username"]] = new_conn

            else:
                sock = socket.fromfd(fd, socket.AF_INET, socket.SOCK_STREAM)
                message, params = socklib.raw_recv(sock)
                username_table[params["dest"]].send(message)
                if message == socklib.DISCONNECT:
                    poll.unregister(fd)
                    
    except Exception as err:
        server.close()
        raise err