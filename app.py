import tkinter as tk
import tkinter.font as tkFont
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import socket
from socket import SHUT_RDWR
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import json


class App:
    sender = ""
    password = ""
    reciever = ""
    kds_ip = "localhost"
    kds_port = 3000

    def __init__(self, root):
        # Setting title
        self.sender=tk.StringVar()
        self.password=tk.StringVar()
        self.to_var=tk.StringVar()
        root.title("Secure Mail Composer")
        
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
        label_email.place(x=40,y=40,width=70,height=25)
        
        label_password=tk.Label(root)
        label_password["font"] = ft
        label_password["fg"] = "#333333"
        label_password["justify"] = "right"
        label_password["text"] = "Password:"
        label_password.place(x=40,y=90,width=70,height=25)
        
        label_To=tk.Label(root)
        label_To["font"] = ft
        label_To["fg"] = "#333333"
        label_To["justify"] = "right"
        label_To["text"] = "To:"
        label_To.place(x=40,y=140,width=70,height=25)
        
        label_Subject=tk.Label(root)
        label_Subject["font"] = ft
        label_Subject["fg"] = "#333333"
        label_Subject["justify"] = "right"
        label_Subject["text"] = "Subject:"
        label_Subject.place(x=40,y=190,width=70,height=25)
        
        self.email_From=tk.Entry(root, textvariable = self.sender)
        self.email_From["borderwidth"] = "1px"
        self.email_From["font"] = ft
        self.email_From["fg"] = "#333333"
        self.email_From["justify"] = "left"
        self.email_From["text"] = "Email"
        self.email_From.place(x=120,y=40,width=420,height=30)
        
        self.email_password=tk.Entry(root, textvariable = self.password, show="*")
        self.email_password["borderwidth"] = "1px"
        self.email_password["font"] = ft
        self.email_password["fg"] = "#333333"
        self.email_password["justify"] = "left"
        self.email_password["text"] = "Password"
        self.email_password.place(x=120,y=90,width=420,height=30)
        
        self.email_To=tk.Entry(root, textvariable = self.to_var)
        self.email_To["borderwidth"] = "1px"
        self.email_To["font"] = ft
        self.email_To["fg"] = "#333333"
        self.email_To["justify"] = "left"
        self.email_To["text"] = "To"
        self.email_To.place(x=120,y=140,width=420,height=30)
        
        self.email_Subject=tk.Entry(root)
        self.email_Subject["borderwidth"] = "1px"
        self.email_Subject["font"] = ft
        self.email_Subject["fg"] = "#333333"
        self.email_Subject["justify"] = "left"
        self.email_Subject["text"] = "Subject"
        self.email_Subject.place(x=120,y=190,width=417,height=30)
        
        self.email_Body=tk.Text(root)
        self.email_Body["borderwidth"] = "1px"
        self.email_Body["font"] = ft
        self.email_Body["fg"] = "#333333"
        self.email_Body.place(x=50,y=240,width=500,height=202)
        
        button_Send=tk.Button(root)
        button_Send["bg"] = "#f0f0f0"
        button_Send["font"] = ft
        button_Send["fg"] = "#000000"
        button_Send["justify"] = "center"
        button_Send["text"] = "Send"
        button_Send.place(x=470,y=460,width=70,height=25)
        button_Send["command"] = self.button_Send_command
        
    def button_Send_command(self):
        self.sender = self.email_From.get()
        # self.password = self.email_password.get()
        self.reciever=self.email_To.get()
        subject = self.email_Subject.get()
        body = self.email_Body.get("1.0","end")
        att="Place holder for the key"
        self.send_email(subject, body,att, self.reciever)
    
    def send_email(self, subject, body, attach, recipients):
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = recipients
        msg.attach(MIMEText("This is dummy email"))

        smtp_server = smtplib.SMTP("smtp-mail.outlook.com", port=587)
        print("Connected")
        smtp_server.starttls()
        print("TLS successful")
        
        try:
            smtp_server.login(self.sender, self.email_password.get())
            print("Login successful")
        except Exception as e:
            print(e)
            print("Login failed, aborted sending email")
            return
        
        # Get the key from KDS
        self.getKey_from_kds()
        
        try: 
            f = open("users.json", "r", encoding="utf-8")
            users = json.load(f)
            f.close()
        except Exception as e:
             print(e)
             return
       
        print(users)
        self.km_a = users[self.sender]
        
        if (self.ks_a and self.ks_b and self.km_a):
            
            self.ks = self.decrypt_key(self.ks_a, self.km_a)
            print(f"ks: {self.ks}")
            
            part=MIMEApplication(self.encrypt_message(self.ks, body), Name="RealMessageBody.txt")
            part['Content-Disposition']='attachment; filename=RealMessageBody.txt'
            msg.attach(part)
            
            part=MIMEApplication(self.ks_b, Name="wrappedkey.txt")
            part['Content-Disposition']='attachment; filename=wrappedkey.txt'
            msg.attach(part)
        
            smtp_server.sendmail(self.sender, recipients, msg.as_string())
            print("Mail sent")
            smtp_server.quit()
        
        else:
            print("Couldn't recieve encryption keys, aborted sending email")
            return
    
    def getKey_from_kds(self):
        self.connect_to_kds()
        self.send_request()
        self.receive_key()
    
    def connect_to_kds(self):
        self.tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpsock.connect((self.kds_ip, self.kds_port))
        # self.tcpsock.recv(2048)

    def send_request(self):
        # Send the sender email and the recevier email
        self.tcpsock.send(f'{self.sender}\n{self.reciever}\n'.encode())

    def receive_key(self):
        self.ks_a, self.ks_b = self.tcpsock.recv(2048).decode().split("\n")
        
        print(f"ks_a: {self.ks_a}")
        print(f"ks_b: {self.ks_b}")
    
    def encrypt_message(self, key, message, chunk_size=16):
        encryptor = AES.new(bytes.fromhex(key), AES.MODE_ECB)
        message_padded = pad(message.encode(), AES.block_size)
        encrypted_message = encryptor.encrypt(message_padded)
        return encrypted_message.hex()
    
        # temp = len(message) % chunk_size
        # padding = 0 if temp == 0 else (chunk_size - temp)
        # message = (message + (' ' * padding))
        # encrypted_message = ''
        # message_bytes = (message + '0'*(chunk_size - len(message.encode()) % chunk_size)).encode()
        # encrypted_message = encryptor.encrypt(message_bytes[:chunk_size])
        # for i in range(chunk_size, len(message), chunk_size):
        
    def decrypt_key(self, encrypted_key, master_key):
        decryptor = AES.new(bytes.fromhex(master_key), AES.MODE_ECB)
        key = decryptor.decrypt(bytes.fromhex(encrypted_key))
        return key.hex()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()