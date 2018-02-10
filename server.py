from socket import *
from threading import *
import os
import time

#Konstante
address = 'localhost'
port = 10000

#Varijable
#Lista klijenata(threads)
clients = []
FILE_PATH = os.getcwd()

def log_file(string):
    with open(FILE_PATH + '/srv_log.txt','a') as f:
        f.write(string)

def client_handle(sock):
    #Prihvatanje korisnickog imena
    username = sock.recv(4096).decode()
    print("<{}> is connected".format(username))
    localtime = time.asctime(time.localtime(time.time()))
    log_string = "({})<{}> is connected".format(localtime,username)
    log_file(log_string)
    clients.append(sock)
    while True:
        try:
            message = sock.recv(1024).decode()
            if not message in ('q','Q'):
                localtime = time.asctime(time.localtime(time.time()))
                log_string = "({})<{}>:{}\n".format(localtime,username,message)
                log_file(log_string)
                send_to_all = "<{}>:{}".format(username,message)
                for client in clients:
                    client.send(send_to_all.encode())
                    # print(client)
            else:
               # Poruka za slanje
               dc_message = 'User {} has disconnected'.format(username)
               localtime = time.asctime(time.localtime(time.time()))
               log_string = '({})User {} has disconnected\n'.format(localtime,username)
               log_file(log_string)
               print(dc_message)
               # Brisanje soketa iz liste soketa
               clients.remove(sock)
               # Obavestavanje ostalih klijenata da je klijent napustio chat
               for client in clients:
                   client.send(dc_message.encode())
               # Zatvaranje soketa
               sock.close()
               # Izlazak iz beskonacne petlje
               break
        except:
            print("Doslo je do nasilnog prekida konekcije..")
            break
def main():
    #Inicijalizacija soketa
    srv_sock = socket(AF_INET,SOCK_STREAM)
    #Konfigurisanje soketa
    srv_sock.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
    try:
        srv_sock.bind((address,port))
    except:
        print("Unaailable to connect to this port..")
        srv_sock.close()
        main()
    #Server sada osluskuje
    srv_sock.listen(5)
    print("Now listening...")

    while True:
        #Prihvatanje konekcije klijenta
        cl_sock, cl_addr = srv_sock.accept()
        #Ispisivanje konektovanog klijenta
        print("{}:{} connected!".format(cl_addr[0],cl_addr[1]))
        t = Thread(target=client_handle,args=(cl_sock,))
        t.start()



if __name__ == '__main__':
    main()
