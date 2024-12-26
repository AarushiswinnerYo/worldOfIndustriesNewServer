import socket
import threading
import os
HEADER=64
PORT=5555
SERVER="0.0.0.0"
ADDR=(SERVER, PORT)
FORMAT='utf-8'
DISCONNECT_MSG="!disconnect"

connectedUsers=[]

ipToUser={}

def cscreen():
    os.system("clear")
    print(f"[ACTIVE THREADS] {len(connectedUsers)}")
    print("Users online:")
    for i in connectedUsers:
        print(i)

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDR)

def handleClient(conn, addr):
    connected=True
    while connected:
        cscreen()
        msg_len=conn.recv(HEADER).decode(FORMAT)
        if msg_len:
            msg_len=int(msg_len)
            msg=conn.recv(msg_len).decode(FORMAT)
            x=msg.split("-")
            if x[0]=="user":
                connectedUsers.append(x[1])
                ipToUser[addr[0]]=x[1]
                print(f"{x[1] Joined the Chat! (Game that is...)")
                conn.send(f"Handshake Made with user:- {x[1]}".encode(FORMAT))
            elif x[0]=="buy":
                conn.send("bought".encode(FORMAT))
            elif msg==DISCONNECT_MSG:
                connected=False
                name=ipToUser[addr[0]]
                nameIndex=connectedUsers.index(name)
                connectedUsers.pop(nameIndex)
                cscreen()
                conn.send(f"Disconnecting user...{ipToUser[addr[0]]}".encode(FORMAT))
            else:
                print(f"[{addr}] {msg}")
                conn.send(f"{msg} received".encode(FORMAT))
    conn.close()

def start():
    global thread
    server.listen()
    print(f"[LISTEN] Listening on {server.getsockname()}")
    while True:
        cscreen()
        conn, addr=server.accept()
        thread=threading.Thread(target=handleClient, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE THREADS] {threading.active_count()-1}")


print("[STARTING] Starting Server...")
start()
