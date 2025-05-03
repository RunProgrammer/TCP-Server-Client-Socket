import socket
import threading
import os
import time



HEADER = 128 #Header size for the message
FORMAT = 'utf-8' #Format of the message
#TODO:DEFINING PROTS AND SERVER ADDRESS
PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())  # Get the server's IP address
Addr = (SERVER, PORT)  # Create a tuple with the server's IP address and port number
DISCONNECT = "!DISCONNECT!"



#TODO:CREATING A SOCKET (TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket


#TODO: BINDING THE SOCKET TO THE ADDr
server.bind(Addr)



def handleConnection(conn , addr):
    
    print(f"[NEW CONNECTION] {addr} connected. \n")
    # print("Hi there! : ) \n")
    
    connectedCheck = True
    while connectedCheck:
        #Read the header(length of the msg)
        msgLength = conn.recv(HEADER).decode(FORMAT) #recives lenth in bytes of padding
        
        if msgLength:
            msgLength = int(msgLength.strip())
            #Reads the main body of the msg
            msg = conn.recv(msgLength).decode(FORMAT)
        

        print(f"{addr} says : {msg} \n")

        connectedCheck = False
        if msg == DISCONNECT:
            connectedCheck = False
        
    conn.close() #Closes the connection with the client
            


def startServer():
    
    server.listen() #Listeing to the incoming connections

    while True:
        #It returns the connection (port and address) of the client
        connection , addr = server.accept() #Accepts the connection from the clients
        
        # print(addr)
        

        #creates a thread for each connection
        threadIt = threading.Thread(target=handleConnection, args=(connection , addr)) 

        #Starting the thread
        threadIt.start()

        #Prints the number of active connections
        # print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1} \n") 
        #As the thread already starting one connection , we need to subtarct it by 1



print(f"<STARTING SERVER> .... :) {Addr} \n")
print("")
startServer()