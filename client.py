import socket
from colorama import init
from termcolor import colored
init(autoreset=True) #Initialize colorama to reset colors after each print


HEADER = 128 #Header size for the message
FORMAT = 'utf-8' #Format of the message

PORT = 5000
DISCONNECT = "!DISCONNECT!"
SERVER = "169.254.74.144"
ADDR = (SERVER, PORT)

CLIENT_SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
CLIENT_SOC.connect(ADDR) #Connects to the server with the defined address and port


def msgFormatter(msg):
    message = msg.encode(FORMAT) 
    msgLen = len(message)
    print(f"Length of the message is : {msgLen}")
    sendLen = str(msgLen).encode(FORMAT)
    sendLen += b' ' * (HEADER - len(sendLen)) 
    
    return sendLen, message


def send(msg):

    sendLen, message = msgFormatter(msg) #Format the message to be sent
    CLIENT_SOC.send(sendLen)
    CLIENT_SOC.send(message)
    print("Message Sent !")

    MsgRecv = CLIENT_SOC.recv(2048).decode(FORMAT)
    print(MsgRecv) 


def disconnect(msg):

    sendLen, message = msgFormatter(msg) #Format the message to be sent
    CLIENT_SOC.send(sendLen)
    CLIENT_SOC.send(message)
    CLIENT_SOC.close()
    print(colored("Disconnected from the server ...", 'red'))

        


if __name__ == "__main__":
    while True:
        print(colored("WELCOME TO THE CLIENT SIDE", 'green'))
        print("")
        print("1. Send a message")
        print("2. Disconnect from the server")
        print("")
        askInput = input(colored("Select an option (1-3): ", 'yellow'))
        if askInput == "1":
            msg = input("Enter your message: ")
            send(msg)
        elif askInput == "2":
            disconnect(DISCONNECT)
            break
        else:
            print(colored("Invalid option. Please try again.", 'red'))
    
        





