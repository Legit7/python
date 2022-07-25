import subprocess
import socket
from threading import *
from time import sleep
import sys
client = False
server = False
port = 54545
name = input("Enter your name: ") + ": "
try:
    if '.' in sys.argv[1]:
        server_ip = sys.argv[1]
        client = True
        try:
            port = sys.argv[2]
            print(f"Connecting to IP: {server_ip} and port: {port}")
        except:
            print(f"Connecting to IP: {server_ip} and port: {port}")
    elif '.' not in sys.argv[1]:
        port = sys.argv[1]
        ip = subprocess.check_output("""ifconfig | grep -w "inet" | grep -v "127.0.0.1" | grep -w "broadcast" | sed "s/^ *//g" | cut -d " " -f 2""",shell=True).decode().replace('\n','')
        print(f"Request a client connection to IP: {ip} and port: {port}")
        server = True
except Exception as e:
    server = True
    ip = subprocess.check_output("""ifconfig | grep -w "inet" | grep -v "127.0.0.1" | grep -w "broadcast" | sed "s/^ *//g" | cut -d " " -f 2""",shell=True).decode().replace('\n','')
    print(f"Request a client connection to IP: {ip} and port: {port}")

if server == True:
    s = socket.socket() # uses IPv4, TCP as default args, can also mention IPv6, UDP 
    s.bind((ip, port)) # server will bind the connection
    s.listen(3) # maximum number of listeners
    conn_list = []
    conn = s.accept() # looks out for client connection and accepts it                                                           
    print("Connected to ", conn)
    conn_list.append(conn)

    # Watch out for incoming connections from clients
    class Conn(Thread):
        def run(self):
            while True:
                conn_list.append(s.accept())
                print('Connected to: ', conn_list[-1])
                sleep(1)

    # Watch out for incoming messages from client
    class Recv(Thread):
        def run(self):
            while True:
                for i in conn_list:
                    tmp, addr = i
                    print(tmp.recv(1024).decode())
                    sleep(0.5)
                    # if len(tmp.recv(1024).decode()) != 0:
                    #     print("At if recv.. ")
                    #     print(tmp.recv(1024).decode())
                    # else:
                    #     print("At else recv.. ")
                    #     continue

    # Watch out for messages to send from server
    class Send(Thread):
        def run(self):
            while True:
                data1 = (name + input()).encode()
                for i in conn_list:
                    tmp1, addr1 = i
                    tmp1.send(data1)
                    sleep(0.5)

    con = Conn()
    recv = Recv()
    send = Send()

    con.start()
    # sleep(1)
    recv.start()
    # sleep(1)
    send.start()

    con.join()
    print("at recv join")
    recv.join()
    print("at send join")
    send.join()

    print("chk1")

    for i in conn_list:
        tmp2, addr = i
        print("\n \nShutting down ", addr,"....")
        tmp2.shutdown()
        print("chk2")
        tmp2.close()
        print("chk3")

if client == True:
    c = socket.socket() # default (IPv4, TCP) optional (IPv6, UDP)
    c.connect((server_ip, port)) # client will use connect method to make connection with given IP and host
    print(f"Connection is ready... \nText out something...")

    # Watch out for messages from server
    class Rec(Thread):
        def run(self):
            while True:
                print(c.recv(1024).decode()) # receives data of 1024 bytes with socket object
                sleep(0.5)

    # Send messages to server
    class Sen(Thread):
        def run(self):
            while True:
                data = (name + input()).encode()
                c.send(data)
                sleep(0.5)

    rec = Rec()
    sen = Sen()

    rec.start()
    # sleep(0.5)
    sen.start()
    rec.join()
    print("at rec join")
    sen.join()
    print("at sen join")
    print("chk1")
    c.shutdown()
    print("chk2")
    c.close()
    print("chk3")
