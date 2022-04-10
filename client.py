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
term = blessed.Terminal()
randomcolor = lambda: random.randint(0, 255)
color = lambda r=randomcolor(), g = randomcolor(), b = randomcolor(): term.color_rgb(r, g, b) # because pretty :)
client = Client(host=hostname if hostname != '' else "",
username=f"{color()}[{username}]" if username != "" else f"{color()}[Guest#{random.randint(1,PORT)}]")
client.send('Intro')
echo = lambda msg: print(msg, end="", flush=True)
row = 7
col = 0
try:
    with term.fullscreen():

        while True:
            echo(term.move_xy(0, 0) + client.username + ": " + term.move_xy(0, 1))
            echo(term.move_y(6) + term.center(color() + "-----Messages:-----" + term.normal) + term.move_xy(0, 1) + color())
            read_recv, _, _ = select.select([client.sock, sys.stdin], [], [])
            for fd in read_recv:
                if fd == client.sock:
                    username, message = client.recv()
                    echo(f"{term.normal}{term.move_y(row)}{message}{term.move_xy(0, 1)}")
                    row += 1
                elif fd == sys.stdin:
                    msg = input()# remove random indent
                    client.send(color()+ msg + term.normal)
                    echo(term.move_xy(0,1) + " " * (term.width * 5) + term.move_xy(0,1) ) # tada

except Exception as err:
    client.send(DISCONNECT)
    client.sock.close()
    raise err
except KeyboardInterrupt:
    print("\nclosing")
    client.send(DISCONNECT)
    client.sock.close()
    

