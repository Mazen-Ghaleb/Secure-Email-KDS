import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import socket
from socket import SHUT_RDWR
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import time

class App:
    kds_ip = "localhost" # IP of the KDS
    kds_port = 3000 # Port of the KDS

    def __init__(self, root): # Initialize the GUI
        self.sender=tk.StringVar() # Sender Email
        self.reciever=tk.StringVar() # Reciever Email
        
        root.title("Secure Mail Composer") # Setting title of the window
        
        # Setting window size
        width=600 
        height=500 
        screenwidth = root.winfo_screenwidth() 
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        
        ft = tkFont.Font(family='Times',size=12) # Font
        
        # Email label
        label_email=tk.Label(root)
        label_email["font"] = ft
        label_email["fg"] = "#333333"
        label_email["justify"] = "right"
        label_email["text"] = "Email:"
        label_email.place(x=40,y=40,width=70,height=25)
        
        # Password label
        label_password=tk.Label(root)
        label_password["font"] = ft
        label_password["fg"] = "#333333"
        label_password["justify"] = "right"
        label_password["text"] = "Password:"
        label_password.place(x=40,y=90,width=70,height=25)
        
        # To label
        label_To=tk.Label(root)
        label_To["font"] = ft
        label_To["fg"] = "#333333"
        label_To["justify"] = "right"
        label_To["text"] = "To:"
        label_To.place(x=40,y=140,width=70,height=25)
        
        # Subject label
        label_Subject=tk.Label(root)
        label_Subject["font"] = ft
        label_Subject["fg"] = "#333333"
        label_Subject["justify"] = "right"
        label_Subject["text"] = "Subject:"
        label_Subject.place(x=40,y=190,width=70,height=25)
        
        # Email entry
        self.email_From=tk.Entry(root, textvariable = self.sender)
        self.email_From["borderwidth"] = "1px"
        self.email_From["font"] = ft
        self.email_From["fg"] = "#333333"
        self.email_From["justify"] = "left"
        self.email_From["text"] = "Email"
        self.email_From.place(x=120,y=40,width=420,height=30)
        
        # Password entry
        self.email_password=tk.Entry(root, show="*")
        self.email_password["borderwidth"] = "1px"
        self.email_password["font"] = ft
        self.email_password["fg"] = "#333333"
        self.email_password["justify"] = "left"
        self.email_password["text"] = "Password"
        self.email_password.place(x=120,y=90,width=420,height=30)
        
        # To entry
        self.email_To=tk.Entry(root, textvariable = self.reciever)
        self.email_To["borderwidth"] = "1px"
        self.email_To["font"] = ft
        self.email_To["fg"] = "#333333"
        self.email_To["justify"] = "left"
        self.email_To["text"] = "To"
        self.email_To.place(x=120,y=140,width=420,height=30)
        
        # Subject entry
        self.email_Subject=tk.Entry(root)
        self.email_Subject["borderwidth"] = "1px"
        self.email_Subject["font"] = ft
        self.email_Subject["fg"] = "#333333"
        self.email_Subject["justify"] = "left"
        self.email_Subject["text"] = "Subject"
        self.email_Subject.place(x=120,y=190,width=417,height=30)
        
        # Body entry
        self.email_Body=tk.Text(root)
        self.email_Body["borderwidth"] = "1px"
        self.email_Body["font"] = ft
        self.email_Body["fg"] = "#333333"
        self.email_Body.place(x=50,y=240,width=500,height=202)
        
        # Send button
        button_Send=tk.Button(root)
        button_Send["bg"] = "#f0f0f0"
        button_Send["font"] = ft
        button_Send["fg"] = "#000000"
        button_Send["justify"] = "center"
        button_Send["text"] = "Send"
        button_Send.place(x=470,y=460,width=70,height=25)
        button_Send["command"] = self.button_Send_command
        
    def button_Send_command(self): # Send button command
        self.sender = self.email_From.get() # Get the sender email
        self.reciever=self.email_To.get() # Get the reciever email
        subject = self.email_Subject.get() # Get the subject of the email
        body = self.email_Body.get("1.0","end") # Get the body of the email 
        att="Place holder for the key" # Place holder for the key
        self.send_email(subject, body,att, self.reciever) # Send the email
    
    def send_email(self, subject, body, attach, recipients):
        msg = MIMEMultipart() # Create a MIMEMultipart object
        msg['Subject'] = subject # Set the subject of the email
        msg['From'] = self.sender # Set the sender of the email
        msg['To'] = recipients # Set the reciever of the email
        msg.attach(MIMEText("This is dummy email")) # Attach the body of the email

        smtp_server = smtplib.SMTP("smtp-mail.outlook.com", port=587) # Create a SMTP object
        print("Connected") # Print connected
        smtp_server.starttls() # Start TLS
        print("TLS successful") # Print TLS successful
        
        try: # Try to login to the email
            smtp_server.login(self.sender, self.email_password.get()) # Login to the email
            print("Login successful") # Print login successful
        except Exception as e: # If login failed
            print(e) # Print the error
            self.show_alert_box("Login failed, aborted sending email") # Show alert box
            print("Login failed, aborted sending email") # Print login failed
            return
        
        self.getKey_from_kds() # Get the key from KDS

        try: # Try to encrypt the body of the email
            time.sleep(1) # Wait 1 second for the kds to write the key to the file
            found = False # Set found to false
            f = open("users.csv", "r") # Open the users.csv file
            for line in f.readlines(): # For each line in the file
                username, master_key = line.strip().split(',') # Split the line into username and master key
                if username == self.sender: # If the username is the sender
                    self.km_a = master_key # Set the master key
                    found = True # Set found to true
                    break # Break out of the loop
            f.close() # Close the file
            if not found: # If the master key was not found
                self.show_alert_box("Couldn't find master key for this email, aborted sending email") # Show alert box
                return
        except Exception as e:
             print("Execption :", e)
             self.show_alert_box("Couldn't find master key for this email, aborted sending email") # Show alert box
             return
        
        if (self.ks_a and self.ks_b and self.km_a): # If the keys were recieved
            
            self.ks = self.decrypt_key(self.ks_a, self.km_a) # Decrypt the key
            print(f"ks: {self.ks}") # Print the key
            
            part=MIMEApplication(self.encrypt_message(self.ks, body), Name="RealMessageBody.txt") # Encrypt the body of the email
            part['Content-Disposition']='attachment; filename=RealMessageBody.txt' # Set the name of the file
            msg.attach(part) # Attach the encrypted body of the email
            
            part=MIMEApplication(self.ks_b, Name="wrappedkey.txt") # Attach the encrypted key
            part['Content-Disposition']='attachment; filename=wrappedkey.txt' # Set the name of the file
            msg.attach(part) # Attach the encrypted key
        
            smtp_server.sendmail(self.sender, recipients, msg.as_string()) # Send the email
            self.show_alert_box("Mail was sent successfully") # Show alert box
            print("Mail sent") # Print mail sent
            smtp_server.quit() # Quit the SMTP server
        
        else: # If the keys were not recieved
            self.show_alert_box("Couldn't recieve encryption keys, aborted sending email") # Show alert box
            print("Couldn't recieve encryption keys, aborted sending email") # Print couldn't recieve encryption keys
            return
    
    def getKey_from_kds(self): # Get the key from KDS
        self.connect_to_kds() # Connect to KDS
        self.send_request() # Send the request
        self.receive_key() # Recieve the key
    
    def connect_to_kds(self): # Connect to KDS
        self.tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
        self.tcpsock.connect((self.kds_ip, self.kds_port)) # Connect to the KDS

    def send_request(self): # Send the request
        self.tcpsock.send(f'{self.sender}\n{self.reciever}\n'.encode()) # Send the sender email and the recevier email

    def receive_key(self): # Recieve the key
        self.ks_a, self.ks_b = self.tcpsock.recv(2048).decode().split("\n") # Recieve the key
        
        print(f"ks_a: {self.ks_a}") # Print the session key encrypted by the sender's master key
        print(f"ks_b: {self.ks_b}") # Print the session key encrypted by the reciever's master key
    
    def encrypt_message(self, key, message, chunk_size=16): # Encrypt the message
        encryptor = AES.new(bytes.fromhex(key), AES.MODE_ECB) # Create an AES object
        message_padded = pad(message.encode(), AES.block_size) # Pad the message
        encrypted_message = encryptor.encrypt(message_padded) # Encrypt the message
        return encrypted_message.hex() # Return the encrypted message as hex
        
    def decrypt_key(self, encrypted_key, master_key): # Decrypt the key
        decryptor = AES.new(bytes.fromhex(master_key), AES.MODE_ECB) # Create an AES object
        key = decryptor.decrypt(bytes.fromhex(encrypted_key)) # Decrypt the key
        return key.hex() # Return the key as hex
    
    def show_alert_box(self, message): # Function to display the alert box
        messagebox.showinfo("Alert", message) # Show the alert box
        
if __name__ == "__main__": # If the file is run directly
    """
    Main method.
    """
    root = tk.Tk() # Create a Tk object
    app = App(root) # Create an App object
    root.mainloop() # Run the main loop