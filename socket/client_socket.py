import socket
from threading import *
from time import sleep

c = socket.socket() # default (IPv4, TCP) optional (IPv6, UDP)

c.connect(('127.0.0.1', 9999)) # client will use connect method to make connection with given IP and host

print("Text it out.....")

class Rec(Thread):
    def run(self):
        while True:
            print("Ser: ", c.recv(1024).decode()) # receives data of 1024 bytes with socket object
            sleep(1)

class Sen(Thread):
    def run(self):
        while True:
            data = input().encode()
            c.send(data)
            sleep(1)

rec = Rec()
sen = Sen()

rec.start()
sleep(1)
sen.start()

rec.join()
sen.join()

c.shutdown()
c.close()

