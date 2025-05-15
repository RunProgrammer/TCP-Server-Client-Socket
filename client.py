import socket
import ssl
from colorama import init
from termcolor import colored
init(autoreset=True)

PORT = 5000
HEADER = 256
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
Addr = (SERVER, PORT)
FLAGS = ["PING", "DISCONNECT", "SEND", "RECEIVE", "LOGIN", "REGISTER"]

# sslContext = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
# sslContext.load_verify_locations(cafile="ecc-ca.pem")  # Load the CA certificate
# sslContext.verify_mode = ssl.CERT_NONE  # Ensure the server certificate is verified
# sslContext.check_hostname = False  # Check the server's hostname against the certificate


clientSOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # USING IPV4 WITH TCP
# clientSOC = sslContext.wrap_socket(rawSOC , server_hostname=SERVER)
clientSOC.connect(Addr)

msgParameters = {
    "flag": None,
    "message": None
}



def getRegister():
    askUsername = input(colored("Enter your username: ", 'blue'))
    askPassword = input(colored("Enter your password: ", 'blue'))
    return askUsername, askPassword


def getLogin():
    askUsername = input(colored("Enter your username: ", 'blue'))
    askPassword = input(colored("Enter your password: ", 'blue'))
    return askUsername, askPassword


def recv():
    msg_length = clientSOC.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length.strip())
        msg = clientSOC.recv(msg_length).decode(FORMAT)
        msg = msg.split('|')
        return msg
    else:
        print(colored("[ERROR] Message length is empty", 'red'))
        clientSOC.close()


def send(msg):
    try:
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))  # Padding to ensure the correct header size
        clientSOC.send(send_length)
        clientSOC.send(message)
    except Exception as e:
        print(f"Error sending message: {e}")
        clientSOC.close()  # Close the connection if sending fails

if __name__ == "__main__":
    print(colored("[STARTING] Client is starting...", 'green'))
    try:
        while True:
            print(colored(FLAGS, 'red'))
            msgParameters["flag"] = input(colored("Enter the flag: ", 'yellow')).upper()
            # msgParameters["message"] = input(colored("Enter the message: ", 'yellow'))
            # combinedMsg = f"{msgParameters['flag']}|{msgParameters['message']}"
            # send(combinedMsg)
            # print(colored(f"[MESSAGE SENT] {msgParameters['flag']} {msgParameters['message']}", 'green'))
            if msgParameters["flag"] == FLAGS[0]:
                msgParameters["message"] = "PINGED ..."
                combinedMsg = f"{msgParameters['flag']}|{msgParameters['message']}"
                send(combinedMsg)
                msgRcv = clientSOC.recv(HEADER).decode(FORMAT)
                print(colored(f"[MESSAGE RECEIVED] {msgRcv}", 'blue'))
                # print(colored(f"[PING] {msgParameters['flag']} {msgParameters['message']}", 'green'))
            
            if msgParameters["flag"] == FLAGS[2]:
                msgParameters["message"] = input(colored("Enter the message: ", 'yellow'))
                combinedMsg = f"{msgParameters['flag']}|{msgParameters['message']}"
                send(combinedMsg)
                msgRcv = clientSOC.recv(HEADER).decode(FORMAT)
                print(colored(msgRcv, 'blue'))

            if msgParameters["flag"] == FLAGS[3]:
                
                msgParameters["message"] = "Client is receiving..."
                combinedMsg = f"{msgParameters['flag']}|{msgParameters['message']}"
                send(combinedMsg)
                msgRcv = clientSOC.recv(HEADER).decode(FORMAT)
                print(colored(msgRcv, 'blue'))

            if msgParameters["flag"] == FLAGS[4]:
                userName , password = getLogin()
                msgParameters["message"] = f"{userName}:{password}"
                combinedMsg = f"{msgParameters['flag']}|{msgParameters['message']}"
                send(combinedMsg)
                msgRecv = clientSOC.recv(HEADER).decode(FORMAT) 
                print(colored(msgRecv,'green'))
            
            
            if msgParameters["flag"] == FLAGS[5]:
                # msgParameters["flag"] = input(colored("Enter the flag: ", 'yellow'))
                userName , password = getRegister()
                msgParameters["message"] = f"{userName}:{password}"
                combinedMsg = f"{msgParameters['flag']}|{msgParameters['message']}"
                send(combinedMsg)
                msgRecv = clientSOC.recv(HEADER).decode(FORMAT) 
                print(colored(msgRecv,'green'))
            
            if msgParameters["flag"] == FLAGS[1]:
                print(colored("[DISCONNECTING] Client is disconnecting...", 'red'))
                msgParameters["message"] = "Client is disconnecting"
                combinedMsg = f"{msgParameters['flag']}|{msgParameters['message']}"
                send(combinedMsg)
                clientSOC.close()
                exit()
    except Exception as e:
        print(f"Error in client: {e}")
    