import socket
import time


HEADER = 128 #Header size for the message
FORMAT = 'utf-8' #Format of the message
#TODO:DEFINING PROTS AND SERVER ADDRESS
PORT = 5000
DISCONNECT = "!DISCONNECT!"
SERVER = "169.254.74.144"
ADDR = (SERVER, PORT)

CLIENT_SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
CLIENT_SOC.connect(ADDR) #Connects to the server with the defined address and port

