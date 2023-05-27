import secrets
from Crypto.Cipher import AES

class KeyManager:
    def __init__(self):
        """
        Initialize the KeyManager class.
        - Set the path to the file storing user information.
        - Create an empty dictionary to store user -> master key mapping.
        - Load existing user information from file if exists.
        """
        self.users_file_path = "users.csv" # Path to the file storing user information
        self.users = {} # Dictionary to store user -> master key mappings
        self.load_users() # Load existing user information from file
        
    def load_users(self):
        """
        Load existing user information from the file if exists.
        - Read each line in the file.
        - Split the line to extract the username and master key.
        - Store the user -> master key mapping in the dictionary.
        """
        try:
            f = open(self.users_file_path, "r") # Open the file
            for line in f.readlines(): # Read each line
                username, master_key = line.strip().split(',') # Split the line into username and master key
                self.users[username] = master_key # Store user -> master key mapping
            f.close() # Close the file
        except Exception as e: # If the file doesn't exist or an exception occurs
            # print("Execption :", e)
            pass

    def save_users(self): # Save the user information to file
        """
        Save the user information to the file.
        - Prepare lines containing the user and master key.
        - Write the lines to the users file or create file if file doesn't exist.
        """
        lines = [] # List to store lines to write to file
        for user in self.users: # For each user
            lines.append(f'{user},{self.users[user]}\n') # Format user and master key as a line
        f = open(self.users_file_path, "w") # Open the file
        f.writelines(lines) # Write the lines to the file
        f.close() # Close the file
    
    def register_user(self, email):
        """
        Register a new user or retrieve the master key if the user already exists.
        - If the user already exists, return their existing master key.
        - Generate a new random key for the user.
        - Store the user -> master key mapping in the dictionary.
        """
        if email in self.users: # If user already exists, return their existing master key
            return self.users[email]
        key = secrets.token_bytes(16).hex() # Generate a new master key
        self.users[email] = key # Store user -> master key mapping
        return key
     
    def get_encrypted_key(self, sender_key, recipient_key):
        """
        Generate a new random session key and encrypt it for the sender and recipient.
        - Generate a new random session key.
        - Encrypt the key using the sender's master key.
        - Encrypt the key using the recipient's master key.
        - Return the encrypted keys for the sender and recipient.
        """
        key = secrets.token_bytes(16).hex() # Generate a new random key
        print(f"ks: {key}")
        encrypted_key_sender = self.encrypt_key(key, sender_key) # Encrypt the key with the sender's master key
        encrypted_key_recipient = self.encrypt_key(key, recipient_key) # Encrypt the key with the recipient's master key
        return encrypted_key_sender, encrypted_key_recipient
    
    def encrypt_key(self, key, master_key):
        """
        Encrypt a key using AES encryption and a master key.
        - Create an AES encryptor with the master key.
        - Encrypt the key using AES encryption.
        - Convert the encrypted key to a hex format.
        - Return the encrypted key.
        """
        encryptor = AES.new(bytes.fromhex(master_key), AES.MODE_ECB) # Create AES encryptor with master key
        encrypted_key = encryptor.encrypt(bytes.fromhex(key)) # Encrypt key using AES
        return encrypted_key.hex()  # Convert encrypted key to hex format and return