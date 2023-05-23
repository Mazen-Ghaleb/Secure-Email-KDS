import secrets
from Crypto.Cipher import AES
import json

class KeyManager:
    def __init__(self):
        f = open("users.json", "r")
        self.users = json.load(f)
        f.close()
        
    def save_users(self):
        f = open("users.json", "w")
        json.dump(self.users, f)
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
    
