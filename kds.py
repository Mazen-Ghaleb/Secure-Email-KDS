import socket, threading
from key_manager import KeyManager

key_mgr = KeyManager()

class ClientThread(threading.Thread):
    
    def __init__(self,ip,port,clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.csocket = clientsocket
        print ("[+] New thread started for ",ip,":",str(port))
    
    def run(self):
        print ("Connection from : ",ip,":",str(port))        
        data = self.csocket.recv(2048)
        messages = data.decode().split("\n")
        
        print("Client(%s:%s) sent : %s"%(self.ip, str(self.port), messages[0]))
        print("Client(%s:%s) sent : %s"%(self.ip, str(self.port), messages[1]))

        sender = messages[0]
        receiver = messages[1]

        # TODO: Critical section
        km_a = key_mgr.register_user(sender)
        km_b = key_mgr.register_user(receiver)
        
        ks_a, ks_b = key_mgr.get_encrypted_key(km_a, km_b)
        print(f"ks_a: {ks_a}")
        print(f"ks_b: {ks_b}")
        
        self.csocket.send(f'{ks_a}\n{ks_b}'.encode())
        self.csocket.close()
        # TODO: Critical section
        key_mgr.save_users()
        print ("Client at ", self.ip," disconnected...")
        
        
host = "localhost"
port = 3000

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcpsock.bind((host,port))

while True:
    tcpsock.listen(4)
    print ("Listening for incoming connections...")
    (clientsock, (ip, port)) = tcpsock.accept()
    # Pass clientsock to the ClientThread thread object being created
    newthread = ClientThread(ip, port, clientsock)
    newthread.start()