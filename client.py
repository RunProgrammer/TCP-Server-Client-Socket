import socket
import time


HEADER = 128 #Header size for the message
FORMAT = 'utf-8' #Format of the message
#TODO:DEFINING PROTS AND SERVER ADDRESS
PORT = 5000
DISCONNECT = "!DISCONNECT!"
SERVER = "###.###.###.###"
ADDR = (SERVER, PORT)

CLIENT_SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
CLIENT_SOC.connect(ADDR) #Connects to the server with the defined address and port


def send(msg):

    message = msg.encode(FORMAT)
    msgLen = len(message) #Calculates the length of the message
    print(msgLen)
    sendLen = str(msgLen).encode(FORMAT)
    sendLen += b' ' * (HEADER - len(sendLen))
    CLIENT_SOC.send(sendLen)
    CLIENT_SOC.send(message)

    print("Message Sent !")

    MsgRecv = CLIENT_SOC.recv(2048).decode(FORMAT)
    print(MsgRecv) 

send("First Message :)")





