import secrets
from Crypto.Cipher import AES
import json

class KeyManager:
    def __init__(self):
        self.users_file_path = "users.csv"
        self.users = {}
        self.load_users()
        
    def load_users(self):
        try:
            f = open(self.users_file_path, "r")
            for line in f.readlines():
                username, master_key = line.strip().split(',')
                self.users[username] = master_key
            f.close()
        except:
            pass

    def save_users(self):
        lines = []
        for user in self.users:
            lines.append(f'{user},{self.users[user]}\n')
        f = open(self.users_file_path, "w")
        f.writelines(lines)
        f.close()
    
    def register_user(self, email):
        if email in self.users:
            return self.users[email]
        key = secrets.token_bytes(16).hex()
        self.users[email] = key
        return key
     
    def get_encrypted_key(self, sender_key, recipient_key):
        key = secrets.token_bytes(16).hex()
        print(f"ks: {key}")
        encrypted_key_sender = self.encrypt_key(key, sender_key)
        encrypted_key_recipient = self.encrypt_key(key, recipient_key)
        return encrypted_key_sender, encrypted_key_recipient
    
    def encrypt_key(self, key, master_key):
        encryptor = AES.new(bytes.fromhex(master_key), AES.MODE_ECB)
        encrypted_key = encryptor.encrypt(bytes.fromhex(key))
        return encrypted_key.hex()
    
