# Author Name : Gautam Baishya
# Email : gautambaishya893@gmail.com
# Date : 15 July 2021

# Important Note: The files on which operations are being performed should be in same folder

#Install pycryptodome 
#command : pip3 install pycryptodome

import os                                   # To provide functions interacting with os. (Handling the Current Working Directory)
from Cryptodome.Cipher import DES3          # cryptodome.cipher package contains secure algorithm to protect the confidentiality of data. DES3 is for encryption 
from hashlib import md5                     # To generate MD5 hash value from a string
from getpass import getpass                 # Used to prompt to users using the string prompt and reads the input from the user as Password. 

from tkinter import *                       # Import something from tkinter library
from tkinter import messagebox              # Used to display the message boxes 
import shelve                               # Used as a simple persistent storage option for Python objects when a relational database is overkill.
  

from tkinter import filedialog              # Offer a set of dialogs that you can use when working with files.


file_path = NONE                            # Get File path in it


key = NONE                                  # Store Password here


radio_input = NONE                          # Get radio button value



window = Tk()                               # Create the root window

def fetchKey(file_path):                    # fetch the dec_key 
    d = shelve.open('enc_keys')
    flag = file_path in d
    
    if(file_path in d):
        return d[file_path]
    else:
        return None
    d.close()


def storeKeys(file_path, enc_key):          # Store the keys    
    basename = os.path.basename(file_path)
    basename = "/Encrypted_"+basename    
    dirname = os.path.dirname(file_path)    
    fpath = dirname + basename    
    d = shelve.open('enc_keys')             # open -- file may get suffix added by low-level                                            
    d[fpath] = enc_key                      # store data at key (overwrites old data if using an existing key)
    d.close()

def InpPwd () :                             # Create an instance of tkinter frame       
        win= Tk()        
        win.geometry("600x250")             # Set the geometry of frame
        def close_win():
            win.destroy()
        
        def chkPwd():
            pwd = password.get()
            cpwd = cpassword.get()
            if(pwd == cpwd) :
                global key 
                key = pwd
                encrypt_decrypt_file()
            else :
                print('Wrong password')
            win.destroy()
            

        
        Label(win,text="Enter the Password", font=('Helvetica',20)).pack(pady=20)               # Create a text label

       
        password= Entry(win,show="*",width=20)                      # Create Entry Widget for password
        password.pack()

       
        Label(win,text="Confirm Password", font=('Helvetica',20)).pack(pady=20)         #Create a text label

        
        cpassword= Entry(win,show="*",width=20)                # Create Entry Widget for password
        cpassword.pack()

        
        Button(win, text="Submit", font=('Helvetica bold',10),command=chkPwd).pack(pady=20)         # Create a button to Chk password and Submit

      
        Button(win, text="Quit", font=('Helvetica bold',10),command=close_win).pack(pady=20)        # Create a button to close the window

        win.mainloop()




def browseFiles():                                  # Function for opening the file explorer window
    global file_path 
    file_path = filedialog.askopenfilename(initialdir = "/home/Desktop",title = "Select a File")
    window.destroy()
    InpPwd()
    
        
            
def encrypt_decrypt_file() :                   # For selecting operation from given choice
    
    while True:
        
        hashing_key = md5(key.encode('ascii')).digest()          # Encode given key to 16 byte ascii key with md5 operation

        
        tdes_key = DES3.adjust_key_parity(hashing_key)            # Adjust key parity of generated Hash Key for Final Triple DES Key
        
        
        cipher = DES3.new(tdes_key, DES3.MODE_EAX, nonce=b'0')    #  Cipher with integration of Triple DES key, MODE_EAX for Confidentiality & Authentication and nonce for generating random / pseudo random number which is used for authentication protocol
       
        with open(file_path, 'rb') as input_file:                  # Open & read file from given path
            file_bytes = input_file.read()
            
            if radio_input == '1':                
                new_file_bytes = cipher.encrypt(file_bytes)        # Perform Encryption operation
                storeKeys(file_path, key)
                filename = os.path.basename(file_path)                
                des_path = "Encrypted_"+filename
                with open(des_path, 'wb') as image_file:
                    image_file.write(new_file_bytes)
                messagebox.showinfo('Encryption', 'Encryption Operation Successful!!Image Saved successfully as filename '+ des_path)
                print('		      Encryption Operation Done!')
                print("")
                print("")
                break
            else:
                
                filename = os.path.basename(file_path)
                enc_key = fetchKey(file_path)                          
                if enc_key == key:                                   # Password Checking                    
                    new_file_bytes = cipher.decrypt(file_bytes)      # Perform Decryption operation             
                    des_path = "Decrypted_"+filename
                    with open(des_path, 'wb') as image_file:
                        image_file.write(new_file_bytes)
                    messagebox.showinfo('Decryption', 'Decryption Operation Successful!!Image Saved successfully as filename '+ des_path)
                    print('		      Decryption Operation Done!')
                    print("")
                    print("")
                    break
                else:
                    messagebox.showerror('Decryption Password Error', 'Wrong password!!! Try Again Later')
                    print('		      Decryption Err pasword Wrong!')
                    break
       
            

      
def MainWindow(): 

    def setVal():
        global radio_input 
        radio_input = str(var.get())

    var = IntVar()                              # Set window title                                                                           
    window.title('File Explorer')
        
    window.geometry("800x400")                  # Set window size
       
    window.config(background = "white")         # Set window background color
        
    label_file_explorer = Label(window, text = "File Explorer using Tkinter", width = 100, height = 4,fg = "blue")     # Create a File Explorer label
            
    button_explore = Button(window, text = "Browse Files",command = browseFiles)
    
    button_exit = Button(window,text = "Exit",command = exit)

    R1 = Radiobutton(window, text="Encrypt", variable=var, value=1, command=setVal)
    R2 = Radiobutton(window, text="Decrypt", variable=var, value=2, command=setVal)

    label_file_explorer.grid(column = 1, row = 1)      # Grid method is chosen for placing the widgets at respective positions in a table like structure by specifying rows and columns
    
    button_explore.grid(column = 1, row = 4)
    
    button_exit.grid(column = 1,row = 7)

    R1.grid(column=1, row=2)
    R2.grid(column=1, row=3)
   
    window.mainloop()                # Let the window wait for any events

MainWindow()       #Main Part
