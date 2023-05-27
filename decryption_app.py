import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
import smtplib
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES

class App:

    def __init__(self, root): # Initialize the GUI
        self.reciever=tk.StringVar() # Reciever Email
        
        root.title("Secure Mail Decrypter") # Setting title of the window
        
        # Setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        
        ft = tkFont.Font(family='Times',size=12)
        
        # Email label
        label_email=tk.Label(root)
        label_email["font"] = ft
        label_email["fg"] = "#333333"
        label_email["justify"] = "right"
        label_email["text"] = "Email:"
        label_email.place(x=20,y=40,width=140,height=25)
        
        # Password label
        label_password=tk.Label(root)
        label_password["font"] = ft
        label_password["fg"] = "#333333"
        label_password["justify"] = "right"
        label_password["text"] = "Password:"
        label_password.place(x=20,y=90,width=140,height=25)
        
        # Encrypted Key label
        label_key=tk.Label(root)
        label_key["font"] = ft
        label_key["fg"] = "#333333"
        label_key["justify"] = "right"
        label_key["text"] = "Encrypted key:"
        label_key.place(x=20,y=140,width=140,height=25)
        
        # Encrypted Message label
        label_Body=tk.Label(root)
        label_Body["font"] = ft
        label_Body["fg"] = "#333333"
        label_Body["justify"] = "right"
        label_Body["text"] = "Encrypted Message:"
        label_Body.place(x=20,y=190,width=140,height=25)
        
        # Decrypted Message label
        label_decryptedBody=tk.Label(root)
        label_decryptedBody["font"] = ft
        label_decryptedBody["fg"] = "#333333"
        label_decryptedBody["justify"] = "right"
        label_decryptedBody["text"] = "Decrypted Message:"
        label_decryptedBody.place(x=20,y=300,width=140,height=25)
        
        # Reciever Email entry
        self.email=tk.Entry(root, textvariable = self.reciever)
        self.email["borderwidth"] = "1px"
        self.email["font"] = ft
        self.email["fg"] = "#333333"
        self.email["justify"] = "left"
        self.email["text"] = "Email"
        self.email.place(x=160,y=40,width=400,height=30)
        
        # Password entry
        self.email_password=tk.Entry(root, show="*")
        self.email_password["borderwidth"] = "1px"
        self.email_password["font"] = ft
        self.email_password["fg"] = "#333333"
        self.email_password["justify"] = "left"
        self.email_password["text"] = "Password"
        self.email_password.place(x=160,y=90,width=400,height=30)
        
        # Encrypted Key entry
        self.key=tk.Entry(root)
        self.key["borderwidth"] = "1px"
        self.key["font"] = ft
        self.key["fg"] = "#333333"
        self.key["justify"] = "left"
        self.key["text"] = "To"
        self.key.place(x=160,y=140,width=400,height=30)
        
        # Encrypted Message entry
        self.email_Body=tk.Text(root)
        self.email_Body["borderwidth"] = "1px"
        self.email_Body["font"] = ft
        self.email_Body["fg"] = "#333333"
        self.email_Body.place(x=160,y=190,width=400,height=101)
        
        # Decrypted Message entry
        self.email_decryptedBody=tk.Text(root, state="disabled")
        self.email_decryptedBody["borderwidth"] = "1px"
        self.email_decryptedBody["font"] = ft
        self.email_decryptedBody["fg"] = "#333333"
        self.email_decryptedBody.place(x=160,y=300,width=400,height=101)
        
        # Decrypt button
        button_Decrypt=tk.Button(root)
        button_Decrypt["bg"] = "#f0f0f0"
        button_Decrypt["font"] = ft
        button_Decrypt["fg"] = "#000000"
        button_Decrypt["justify"] = "center"
        button_Decrypt["text"] = "Decrypt"
        button_Decrypt.place(x=300,y=460,width=70,height=25)
        button_Decrypt["command"] = self.button_Decrypt_command
        
    def button_Decrypt_command(self): # Decrypt button command
        self.reciever = self.email.get() # Get the reciever email
        self.ks_b = self.key.get() # Get the encrypted session key
        self.encrypted_message = self.email_Body.get("1.0","end") # Get the encrypted message
        att="Place holder for the key" # Place holder for the key
        if (self.getDecryptionKey()): # If the master key is found
            self.setDecryptedMessage(self.decryptMessage(self.encrypted_message, self.ks)) # Decrypt the message
        else: # If the master key is not found
            self.setDecryptedMessage("") # Set the decrypted message to empty
    
    def getDecryptionKey(self) -> bool: # Get the decryption key
        """
        Gets master key from the csv file if user successfully logs in and key is found in the csv file
        """
        
        smtp_server = smtplib.SMTP("smtp-mail.outlook.com", port=587) # Connect to the smtp server
        print("Connected") # Print connected
        smtp_server.starttls() # Start TLS
        print("TLS successful") # Print TLS successful
        
        try : # Try to login
            smtp_server.login(self.reciever, self.email_password.get()) # Login to the smtp server
            print("Login successful") # Print login successful
        except Exception as e: # If login fails
            print(e) # Print the error
            self.show_alert_box("Login failed, aborted decryption") # Show alert box
            print("Login failed, aborted decryption") # Print login failed
            return False 
        
        try :            
            f = open("users.csv", "r") # Open the csv file
            found = False # Set found to false
            for line in f.readlines(): # For each line in the csv file
                username, master_key = line.strip().split(',') # Get the username and master key
                if username == self.reciever: # If the username matches the reciever email
                    self.km_b = master_key # Set the master key
                    found = True # Set found to true
                    break # Break out of the loop
            f.close() # Close the csv file
            if not found: # If the master key is not found
                self.show_alert_box("Couldn't find master key for this email") # Show alert box
                return
        except  Exception as e: # If an exception occurs
             print("Execption :", e) # Print the exception
             self.show_alert_box(e) # Show alert box
             return
       
        print(f"km_b: {self.km_b}") # Print the master key
        print(f"ks_b: {self.ks_b}") # Print the encrypted session key
        
        self.ks = self.decrypt_key(self.ks_b, self.km_b) # Decrypt the session key
        print(f"ks: {self.ks}") # Print the session key
        
        smtp_server.quit() # Quit the smtp server
        return True 
      
    def decrypt_key(self, encrypted_key, master_key): # Function to decrypt the session key
        decryptor = AES.new(bytes.fromhex(master_key), AES.MODE_ECB) # Create a decryptor
        key = decryptor.decrypt(bytes.fromhex(encrypted_key)) # Decrypt the session key
        return key.hex() # Return the session key as hex
    
    def decryptMessage(self, encrypted_msg, key): # Function to decrypt the message
        decryptor = AES.new(bytes.fromhex(key), AES.MODE_ECB) # Create a decryptor
        decrypted_msg = decryptor.decrypt(bytes.fromhex(encrypted_msg)) # Decrypt the message
        try: # Try to unpad the message
            decrypted_msg = unpad(decrypted_msg, AES.block_size) # Unpad the message
        except: # If an exception occurs then the master key is incorrect
            self.show_alert_box("Incorrect master key") # Show alert box
            print("Incorrect master key") # Print incorrect master key
            return "" # Return empty string
        decrypted_msg = decrypted_msg.decode() # Decode the message
        print("Decrypted Message:\n" + decrypted_msg) # Print the decrypted message
        return decrypted_msg 
    
    def setDecryptedMessage(self, decrypted_msg): # Function to set the decrypted message
        self.email_decryptedBody.config(state="normal") # Enable the widget to modify its contents
        self.email_decryptedBody.delete("1.0", "end") # Delete any existing text in the widget
        self.email_decryptedBody.insert("1.0", decrypted_msg) # Insert the decrypted_msg text into the widget
        self.email_decryptedBody.config(state="disabled") # Disable the widget to prevent further modifications
        
    def show_alert_box(self, message): # Function to display the alert box
        messagebox.showinfo("Alert", message) # Show the alert box
        
if __name__ == "__main__": # If the file is run directly
    """
    Main method.
    """
    root = tk.Tk() # Create a Tk object
    app = App(root) # Create an App object
    root.mainloop() # Run the main loop