import socket

from threading import *
from time import sleep

s = socket.socket() # uses IPv4, TCP as default args, can also mention IPv6, UDP 

s.bind(('127.0.0.1', 9999)) # server will bind the connection
s.listen(3) # maximum number of listeners

conn_list = []

conn = s.accept() # looks out for client connection and accepts it                                                           
print("Connected to ", conn)
conn_list.append(conn)

class Conn(Thread):
    def run(self):
        while True:
            conn_list.append(s.accept())
            print('Connected to: ', conn_list[-1])
            sleep(1)

class Recv(Thread):
    def run(self):
        while True:
            for i in conn_list:
                tmp, addr = i
                if len(tmp.recv(1024).decode()) != 0:

                    print(tmp.recv(1024).decode())
                else:
                    continue

class Send(Thread):
    def run(self):
        while True:
            data1 = input().encode()
            for i in conn_list:
                tmp1, addr1 = i
                tmp1.send(data1)
                sleep(0.8)

con = Conn()
recv = Recv()
send = Send()

con.start()
sleep(1)
recv.start()
sleep(0.2)
send.start()

con.join()
recv.join()
send.join()

for i in conn_list:
    tmp2, addr = i
    print("\n \nShutting down ", addr,"....")
    tmp2.shutdown()
    tmp2.close()


