import select
from socklib import *
import time
import socket
import sys
import blessed

print("CTRL-C to close. Enter to send message.")
username = input("What's your name? (leave blank for anon): " )
hostname = input("Type hostname (leave blank for localhost): ")
# ok pretty much do what it says in the parenthesies above
client = Client(host=hostname if hostname != '' else "",
username=username if username != "" else f"Guest#{random.randint(1,PORT)}")
client.send('Intro')
echo = lambda msg: print(msg, end="", flush=True)
row = 6
col = 0
try:
    term = blessed.Terminal()
    with term.fullscreen():
        echo(term.move_xy(0, 0) + "Type something..." + term.move_xy(0, 1))
        while True:
            read_recv, _, _ = select.select([client.sock, sys.stdin], [], [])
            for fd in read_recv:
                if fd == client.sock:
                    username, message = client.recv()
                    echo(f"{term.move_y(row)}[{username}]: {message}{term.move_xy(0, 1)}")
                    row += 1
                elif fd == sys.stdin:
                    client.send(input())
                    echo(term.move_xy(0,1) + " " * (term.width * 5) + term.move_xy(0,1) ) # tada
except Exception as err:
    client.send(DISCONNECT)
    client.sock.close()
    raise err
except KeyboardInterrupt:
    print("\nclosing")
    client.send(DISCONNECT)
    client.sock.close()
    

