import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
import smtplib
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES
import json

class App:

    def __init__(self, root):
        self.reciever=tk.StringVar()
        
        # Setting title
        root.title("Secure Mail Decrypter")
        
        # Setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        
        ft = tkFont.Font(family='Times',size=12)
        
        label_email=tk.Label(root)
        label_email["font"] = ft
        label_email["fg"] = "#333333"
        label_email["justify"] = "right"
        label_email["text"] = "Email:"
        label_email.place(x=20,y=40,width=140,height=25)
        
        label_password=tk.Label(root)
        label_password["font"] = ft
        label_password["fg"] = "#333333"
        label_password["justify"] = "right"
        label_password["text"] = "Password:"
        label_password.place(x=20,y=90,width=140,height=25)
        
        label_key=tk.Label(root)
        label_key["font"] = ft
        label_key["fg"] = "#333333"
        label_key["justify"] = "right"
        label_key["text"] = "Encrypted key:"
        label_key.place(x=20,y=140,width=140,height=25)
        
        label_Body=tk.Label(root)
        label_Body["font"] = ft
        label_Body["fg"] = "#333333"
        label_Body["justify"] = "right"
        label_Body["text"] = "Encrypted Message:"
        label_Body.place(x=20,y=190,width=140,height=25)
        
        label_decryptedBody=tk.Label(root)
        label_decryptedBody["font"] = ft
        label_decryptedBody["fg"] = "#333333"
        label_decryptedBody["justify"] = "right"
        label_decryptedBody["text"] = "Decrypted Message:"
        label_decryptedBody.place(x=20,y=300,width=140,height=25)
        
        self.email=tk.Entry(root, textvariable = self.reciever)
        self.email["borderwidth"] = "1px"
        self.email["font"] = ft
        self.email["fg"] = "#333333"
        self.email["justify"] = "left"
        self.email["text"] = "Email"
        self.email.place(x=160,y=40,width=400,height=30)
        
        self.email_password=tk.Entry(root, show="*")
        self.email_password["borderwidth"] = "1px"
        self.email_password["font"] = ft
        self.email_password["fg"] = "#333333"
        self.email_password["justify"] = "left"
        self.email_password["text"] = "Password"
        self.email_password.place(x=160,y=90,width=400,height=30)
        
        self.key=tk.Entry(root)
        self.key["borderwidth"] = "1px"
        self.key["font"] = ft
        self.key["fg"] = "#333333"
        self.key["justify"] = "left"
        self.key["text"] = "To"
        self.key.place(x=160,y=140,width=400,height=30)
        
        self.email_Body=tk.Text(root)
        self.email_Body["borderwidth"] = "1px"
        self.email_Body["font"] = ft
        self.email_Body["fg"] = "#333333"
        self.email_Body.place(x=160,y=190,width=400,height=101)
        
        self.email_decryptedBody=tk.Text(root, state="disabled")
        self.email_decryptedBody["borderwidth"] = "1px"
        self.email_decryptedBody["font"] = ft
        self.email_decryptedBody["fg"] = "#333333"
        self.email_decryptedBody.place(x=160,y=300,width=400,height=101)
        
        button_Decrypt=tk.Button(root)
        button_Decrypt["bg"] = "#f0f0f0"
        button_Decrypt["font"] = ft
        button_Decrypt["fg"] = "#000000"
        button_Decrypt["justify"] = "center"
        button_Decrypt["text"] = "Decrypt"
        button_Decrypt.place(x=300,y=460,width=70,height=25)
        button_Decrypt["command"] = self.button_Decrypt_command
        
    def button_Decrypt_command(self):
        self.reciever = self.email.get()
        self.ks_b = self.key.get()
        self.encrypted_message = self.email_Body.get("1.0","end")
        att="Place holder for the key"
        if (self.getDecryptionKey()):
            self.setDecryptedMessage(self.decryptMessage(self.encrypted_message, self.ks))
        else:
            self.setDecryptedMessage("")
    
    def getDecryptionKey(self) -> bool:
        smtp_server = smtplib.SMTP("smtp-mail.outlook.com", port=587)
        print("Connected")
        smtp_server.starttls()
        print("TLS successful")
        
        try:
            smtp_server.login(self.reciever, self.email_password.get())
            print("Login successful")
        except Exception as e:
            print(e)
            self.show_alert_box("Login failed, aborted decryption")
            print("Login failed, aborted decryption")
            return False
        
        try:            
            f = open("users.csv", "r")
            found = False
            for line in f.readlines():
                username, master_key = line.strip().split(',')
                if username == self.reciever:
                    self.km_b = master_key
                    found = True
                    break
            f.close()
            if not found:
                self.show_alert_box("Couldn't find master key for this email")
                return

        except  Exception as e:
             print("Execption :", e)
             self.show_alert_box(e)
             return
       
        print(f"km_b: {self.km_b}")
        print(f"ks_b: {self.ks_b}")
        
        self.ks = self.decrypt_key(self.ks_b, self.km_b)
        print(f"ks: {self.ks}")
        
        smtp_server.quit()
        return True
      
    def decrypt_key(self, encrypted_key, master_key):
        decryptor = AES.new(bytes.fromhex(master_key), AES.MODE_ECB)
        key = decryptor.decrypt(bytes.fromhex(encrypted_key))
        return key.hex()
    
    def decryptMessage(self, encrypted_msg, key):
        decryptor = AES.new(bytes.fromhex(key), AES.MODE_ECB)
        decrypted_msg = decryptor.decrypt(bytes.fromhex(encrypted_msg))
        try:
            decrypted_msg = unpad(decrypted_msg, AES.block_size)
        except:
            self.show_alert_box("Incorrect master key")
            print("Incorrect master key")
            return ""
        decrypted_msg = decrypted_msg.decode()
        print("Decrypted Message:\n" + decrypted_msg)
        return decrypted_msg
    
    def setDecryptedMessage(self, decrypted_msg):
        # Enable the widget to modify its content
        self.email_decryptedBody.config(state="normal")

        # Delete any existing text in the widget
        self.email_decryptedBody.delete("1.0", "end")

        # Insert the decrypted_msg text into the widget
        self.email_decryptedBody.insert("1.0", decrypted_msg)

        # Disable the widget to prevent further modifications
        self.email_decryptedBody.config(state="disabled")
        
    # Function to display the alert box
    def show_alert_box(self, message):
        messagebox.showinfo("Alert", message)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()