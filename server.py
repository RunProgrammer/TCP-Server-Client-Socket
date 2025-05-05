import socket
import threading
from datetime import datetime
from colorama import init
from termcolor import colored
init(autoreset=True) 

HEADER = 128 #Header size for the message
FORMAT = 'utf-8' #Format of the message

PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())  # Get the server's IP address
Addr = (SERVER, PORT)  # Create a tuple with the server's IP address and port number
DISCONNECT = "!DISCONNECT!"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
server.bind(Addr)

def loggHandler(logInfo):
    with open("serverLog.log", "a+") as logFile:
        logFile.write(f"{datetime.now()} :- {logInfo} \n")
        print("Logged")
        


def handleConnection(conn , addr):
    
    print(colored(f"[NEW CONNECTION] {addr} connected. \n", 'green'))
    # print("Hi there! : ) \n")
    
    loggHandler(f"{addr} connected succesfully ..") #Logs the connection 
    
    try:
        connectedCheck = True
        while connectedCheck:
            #Read the header(length of the msg)
            msgLength = conn.recv(HEADER).decode(FORMAT) #recives lenth in bytes of padding

            if msgLength:
                msgLength = int(msgLength.strip())
                #Reads the main body of the msg
                msg = conn.recv(msgLength).decode(FORMAT)


            print(f"{addr} says : {msg} \n")

            if msg == DISCONNECT:
                connectedCheck = False
                loggHandler(f"{addr} disconnected succesfully !!")
                conn.close() #Closes the connection with the client
            else:
                conn.send("Message Recived".encode(FORMAT)) 
    
    except Exception as e:
        print(colored(f"[ERROR] {addr} disconnected with error : {e}", 'red'))
        loggHandler(f"{addr} disconnected with error : {e}")
        conn.close()
            


def startServer():
    
    server.listen() #Listeing to the incoming connections

    while True:
        #It returns the connection (port and address) of the client
        connection , addr = server.accept() #Accepts the connection from the clients
        #creates a thread for each connection
        threadIt = threading.Thread(target=handleConnection, args=(connection , addr)) 

        threadIt.start()

        '''
        if (threading.active_count() - 1) == 1:
            break
            exit(0)
        else:
            continue
        '''

print(colored(f"<STARTING SERVER> .... :) {Addr} \n", 'green'))
print("")
startServer()