from socket import *
from threading import *

#Konstante
address = 'localhost'
port = 10000

def listen(sock):
    print("Listening")
    while True:
        try:
            message = sock.recv(4096).decode()
            if message:
                print(message)
            else:
                return
        except:
            print("Doslo je do nasilnog prekida konekcije")

def send(sock):
    while True:
        try:
            message = input()
            if not message in ('q','Q'):
                sock.send(message.encode())
            else:
                sock.send(message.encode())
                print("Dovidjenja!")
                return
        except:
            print("Doslo je do nasilnog prekida konekcije")
            return
def main():
    sock = socket()
    try:
        sock.connect((address,port))
        username = input("Enter username: ")
        sock.send(username.encode())
        t = Thread(target=listen,args=(sock,))
        t.start()
        s = Thread(target=send,args=(sock,))
        s.start()
    except:
        print("Doslo je do prekida konekcije")
        sock.close()
if __name__=="__main__":
    main()
