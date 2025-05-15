import socket
import ssl
import threading
from colorama import init
from termcolor import colored
from datetime import datetime
init(autoreset=True)

#CONSTANTS
PORT = 5000
HEADER = 256
FORMAT = 'utf-8'

SERVER = socket.gethostbyname(socket.gethostname())
Addr = (SERVER, PORT)
FLAGS = ["PING" , "DISCONNECT" , "SEND" , "RECEIVE" , "LOGIN" , "REGISTER"]

#Creates a ssl/tls context for the server (certificate and key files should be in the same directory)
# sslContext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# sslContext.load_cert_chain(certfile="server.crt", keyfile="server.key")


serverSOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #USING IPV4 WITH UDP    
serverSOC.bind(Addr)



def loggHandler(logInfo):
    with open("serverLog.log", "a+") as logFile:
        logFile.write(f"{datetime.now()} -> {logInfo} \n")
        print("Logged")

def send(msg , conn):
    try:
        print(colored(f"[SEND] {msg}", 'blue'))
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))  # Padding to ensure the correct header size
        conn.send(send_length)
        conn.send(message)
    except Exception as e:
        print(f"Error sending message: {e}")
        conn.close()  


def handleClient(conn, addr):
    print(colored(f"[NEW CONNECTION] {addr} connected.", 'green'))

    loggHandler(f"[NEW CONNECTION] {addr} connected.")
    
    try:
        conntectionCheck = True
        while conntectionCheck:
            # Receive message length
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length.strip())
                msg = conn.recv(msg_length).decode(FORMAT)
                msg = msg.split('|')
                print(msg)

                if msg[0] == FLAGS[0]:
                    print(colored(f"[PING] {addr} is pinged", 'green'))
                    loggHandler(f"{addr} is pinged")
                    conn.send("PINGED".encode(FORMAT))
                
                elif msg[0] == FLAGS[1]:
                    print(colored(f"[DISCONNECTED] {addr} disconnected.", 'red'))
                    # conn.close()  # Close connection gracefully here
                    conntectionCheck = False
                    conn.close()
                    loggHandler(f"{addr} is DISCONNECTED")
                
                elif msg[0] == FLAGS[2]:
                    print(colored(f"[MESSAGE] {addr} sent : {msg[1]}", 'blue'))
                    conn.send("MESSAGE RECEIVED".encode(FORMAT))
                    loggHandler(f"Message sent by {addr} to {Addr}")
                
                elif msg[0] == FLAGS[3]:
                    msgTOsend = "just thinking i solved it"
                    print(colored(f"{addr} is receiving ... ", 'yellow'))
                    conn.send(f"{msgTOsend}".encode(FORMAT))
                    loggHandler(f"Message sent by {Addr} to {addr}")
                    #send("hi sent",conn)
                elif msg[0] == FLAGS[4]:
                    print(colored(f"[LOGIN] {addr} sent : {msg[1]}", 'blue'))
                    uName, uPass = msg[1].split(':')
                    print(colored(f"{uName} is logged IN with the password {(len(uPass) * '*')}",'green'))
                    loggHandler(f"[{FLAGS[5]}] User has been logged IN  by {addr}")     
                    conn.send("User has been loggedIN succesfully ...".encode(FORMAT)) 
                
                elif msg[0] == FLAGS[5]:
                    print(colored(f"[REGISTER] {addr} sent : {msg[1]}", 'blue'))
                    uName, uPass = msg[1].split(':')
                    print(colored(f"{uName} is created with the password {(len(uPass) * '*')}",'green'))
                    loggHandler(f"[{FLAGS[5]}] User has been registerd by {addr}")     
                    conn.send("User has been register succesfully ...".encode(FORMAT))           
                else:
                    print(colored(f"[UNKNOWN FLAG] {addr} sent : {msg[0]}", 'red'))
                    conn.send("Unknown flag".encode(FORMAT))  # Send error message back
                    conntectionCheck = False
                     # Close connection on unknown flag
            else: 
                break  # In case the message length is zero, break the loop

    except Exception as e:
        print(colored(f"[EXCEPTION] {e}", 'red'))
        conntectionCheck = False
    finally:
        conn.close()

    

def startServer():

    serverSOC.listen()

    while True:
        try:
            conn , addr = serverSOC.accept()
            # conn = sslContext.wrap_socket(conn, server_side=True) #wrap the socket with ssl/tls on server side
            # print(conn)
            # print(colored(f"[NEW CONNECTION] {addr} connected.", 'yellow'))
            thread = threading.Thread(target=handleClient , args = (conn, addr))
            thread.start()
            print(colored(f"[ACTIVE CONNECTIONS] {threading.active_count()}" , 'blue'))
        
        except Exception as e:
            print(colored(f"[EXCEPTION] {e}", 'red'))
            break

if __name__ == "__main__":
    print(colored("[STARTING] Server is starting...", 'green'))
    startServer()