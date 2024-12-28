import socket
import threading
import os
import functions
HEADER=64
PORT=5555
SERVER="0.0.0.0"
ADDR=(SERVER, PORT)
FORMAT='utf-8'
DISCONNECT_MSG="!disconnect"

connectedUsers=[]
ipToUser={}

def cscreen():
    os.environ['TERM'] = 'xterm'
    os.system("clear")
    print(f"\033[32m[ACTIVE THREADS] {len(connectedUsers)}\033[0m")
    print("\033[32mUsers online:\033[0m")
    for i in connectedUsers:
        print(f"\033[32m{i}\033[0m")

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
            if x[0]=="signup":
                signRes=functions.signUp(x[1],x[2])
                if signRes=="Done!":
                    conn.send("User signed up successfully".encode(FORMAT))
                    print(f"\033[32mUser:-{x[1]} up successfully\033[0m")
                else:
                    conn.send("Exists".encode(FORMAT))
                    connected=False
            elif x[0]=="login":
                loginRes=functions.login(x[1],x[2])
                if loginRes=="correct!":
                    conn.send("Successfully logged in!".encode(FORMAT))
                    print(f"\033[32mUser:-{x[1]} logged on\033[0m")
                elif loginRes=="User not found!":
                    conn.send("Non-existent".encode(FORMAT))
                    connected=False
                    print(f"{x[1]} tried to login but never existed")
                elif loginRes=="incorrect!":
                    conn.send("Incorrect password".encode(FORMAT))
                    connected=False
            elif x[0]=="user":
                connectedUsers.append(x[1])
                ipToUser[addr[0]]=x[1]
                print(f"\033[32m{x[1]} Joined the Chat! (Game that is...)\033[0m")
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
                print(f"\033[31m{ipToUser[addr[0]]} disconnected :(\033[0m")
            else:
                print(f"\033[32m[{ipToUser[addr[0]]}] {msg}\033[0m")
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
