import socket
from threading import *
from time import sleep

s = socket.socket()
s.bind(('localhost', 9999))
s.listen(5)

conn_list = []
conn_list.append(s.accept())


class Conn(Thread):
    def run(self):
        while True:
            print("type: ", type(conn_list[-1]), conn_list[-1])
            conn_list.append(s.accept())

conn = Conn()
conn.start()

conn.join()

for i in conn_list:
    i.close()
