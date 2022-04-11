import socklib
import socket

server = socket.socket()

server.bind(("localhost", socklib.DEFAULT_PORT))
server.listen(5)

conn = socklib.Server(*server.accept())

print(conn.recv())
conn.send("h")