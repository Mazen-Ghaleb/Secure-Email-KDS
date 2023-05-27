import socket, threading
from key_manager import KeyManager

class ClientThread(threading.Thread):
    """
    Thread class for handling client connections.
    """
    
    def __init__(self, ip, port, clientsocket):
        """
        Initialize the ClientThread class.
        
        Parameters:
        ip: IP address of the client.
        port: Port number of the client connection.
        clientsocket: Client socket object.
        """
        threading.Thread.__init__(self)
        self.ip = ip # IP address of the client
        self.port = port # Port number of the client connection
        self.csocket = clientsocket # Client socket object
        print ("[+] New thread started for ",ip,":",str(port)) # Print the IP address and port number of the client connection
    
    def run(self):
        """
        Method representing the thread's activity.
        It handles the client connection, message exchange, key generation, and encryption.
        """
        print ("Connection from : ",ip,":",str(port)) # Print the IP address and port number of the client connection        
        data = self.csocket.recv(2048) # Receive data from the client
        messages = data.decode().split("\n") # Split the data into two messages
        
        print("Client(%s:%s) sent : %s"%(self.ip, str(self.port), messages[0])) # Print the first message
        print("Client(%s:%s) sent : %s"%(self.ip, str(self.port), messages[1])) # Print the second message

        sender = messages[0] # Extract the sender email
        receiver = messages[1] # Extract the receiver email

        km_a = key_mgr.register_user(sender) # Register the sender email if not registered already
        km_b = key_mgr.register_user(receiver) # Register the receiver email if not registered already
        
        ks_a, ks_b = key_mgr.get_encrypted_key(km_a, km_b) # Generate the encryption keys
        print(f"ks_a: {ks_a}") # Print the first encryption key
        print(f"ks_b: {ks_b}") # Print the second encryption key
        
        self.csocket.send(f'{ks_a}\n{ks_b}'.encode()) # Send the encryption keys to the client
        self.csocket.close() # Close the client socket

        key_mgr.save_users() # Save the users to the file
        print ("Client at ", self.ip," disconnected...") # Print the IP address of the client connection
        
if __name__ == "__main__":
    """
    Main method.
    """
    key_mgr = KeyManager() # Create a KeyManager object
   
    host = "localhost" # Host IP address
    port = 3000 # Host port number

    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Reuse the socket

    tcpsock.bind((host,port)) # Bind the socket to the host IP address and port number

    while True:
        tcpsock.listen(4) # Listen for incoming connections
        print ("Listening for incoming connections...") # Print a message
        (clientsock, (ip, port)) = tcpsock.accept() # Accept a client connection
        
        # Pass clientsock to the ClientThread thread object being created
        newthread = ClientThread(ip, port, clientsock) # Create a new thread for the client connection
        newthread.start() # Start the thread