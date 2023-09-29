## Import Modules
import os
from cryptography.fernet import Fernet

##------------------------------------------------------------------------
# Key Generation Function

def generate_key():
    try:
        key = Fernet.generate_key()    
        with open(key_file,'wb') as file :
            file.write(key)
    except:
        print("\nError in generating the Key file !!!\n")
        exit()

##------------------------------------------------------------------------
# Key Load Function

def load_key():
    try:
        with open(key_file, 'rb') as file:
            key = file.read()
        return key
    except:
        print("\nError in Loading the Key !!!\n")
        exit()

##------------------------------------------------------------------------
# Create Account Function

def create_acc():
    # Username with no leading and trailing white spaces
    user_name = input("\nUsername : ").rstrip().lstrip()

    # Checking username characters length
    if user_name == '' :
        print('Username required !!!')
        return
        
    elif len(user_name) < 3 or len(user_name) > 15 :
        print("Only 3 - 15 characters allowed in Username")
        return
    
    else:
        # Padding with " ", if length < 15
        while len(user_name) < 15:
            user_name = user_name + " "

    user_pwd = input("Password : ")    

    if user_pwd == '':
        print('User Password required !!!')

    elif user_pwd.count(" ") != 0:
        print("\nPassword can't have space!!!")

    elif len(user_pwd) < 4 or len(user_pwd) > 12:
        print("\nPassword must have 4 - 12 characters !!!")
    
    else:
        try:
            with open(passwords_file, 'a') as file:
                # Encrypt and store password
                encrypt_pwd = master_key.encrypt(user_pwd.encode()).decode()
                file.write(f"\n {user_name}  |  {encrypt_pwd}" )
            print("\nUsername with Password saved Successfully.")
        except:
            print("\nError in Writing to 'passwords.txt' file !!!\n")
            exit()

##------------------------------------------------------------------------
# View Data Function

def view_data():
    line_number = 1
    try:
        with open(passwords_file, 'r') as file:
            lines = file.readlines()
            # Checking data
            if len(lines) < 3:
                print("\nNo Data !!!")
                return
            
            # Structred Display
            print("\n----------------------------------------------")
            print("|S.No.|      Username      |     Password    |\n----------------------------------------------")

            for line in lines:
                # Ignoring first 2 lines of file
                if line_number < 3:
                    line_number += 1
                    continue

                data = line.rstrip()
                user_name, user_pwd = data.split("  |  ")
                # Decrypt and read password
                decrypt_pwd = master_key.decrypt(user_pwd.encode()).decode()

                # Padding with " ", if length < 12
                while len(decrypt_pwd) < 12:
                    decrypt_pwd = decrypt_pwd + " "

                if line_number < 12:
                    print(f"| {line_number - 2}.  |  {user_name}  |   {decrypt_pwd}  |")
                else:
                    print(f"| {line_number - 2}. |  {user_name}  |   {decrypt_pwd}  |")

                line_number += 1
            print("----------------------------------------------")
    except:
        print("\nError in Reading from 'passwords.txt' file !!!\n")
        exit()

##------------------------------------------------------------------------
# Access Control

master_pwd = input("\n----- PASSWORD MANAGER -----\n\nMaster Password : ")

if master_pwd != '2023':
    print("\nACCESS DECLINED !!!\nIncorrect Master Password.\n")
    exit()

print("\nACCESS GRANTED !!!\nWelcome\n")

##------------------------------------------------------------------------
## Setting up Password_Manager_Files directory

workingDirectory = os.getcwd()
manager_dir = 'Password_Manager_Files'
path = os.path.join(workingDirectory, manager_dir)

##------------------------------------------------------------------------
# Creating output directory

try:
    if not os.path.exists(path):
        os.makedirs(path)
except:
    print(f"\nError in Creating directory\n")
    exit()

##------------------------------------------------------------------------
# Files

passwords_file = 'Password_Manager_Files/passwords.txt'
key_file = 'Password_Manager_Files/key_file.key'

##------------------------------------------------------------------------
# Initializing password.txt file

if (not os.path.exists(passwords_file)) or os.path.getsize(passwords_file) == 0:
    try:
        with open(passwords_file, 'a') as file:
            file.write("     Username     |     Password    \n------------------------------------------------------------------------------------" )
    except:
        print("\nError in Creating passwords.txt file !!!\n")
        exit()
    
##------------------------------------------------------------------------
# Generate Key_file

if not os.path.exists(key_file):
    generate_key()

##------------------------------------------------------------------------
# Setting up the KEY

key = load_key() + master_pwd.encode()
master_key = Fernet(key)

##------------------------------------------------------------------------
# Menu Driven Display

while True:

    mode = input("\n----- PASSWORD MANAGER -----\n\n1. CREATE Account\n2. VIEW Data\n3. Quit\n\n -->  ")

    if mode == '1':
        create_acc()
        input("\nPress Enter to Continue....")

    elif mode == '2':
        view_data()
        input("\n\nPress Enter to continue....")

    elif mode == '3':
        print("\nThank You !!!\n")
        break

    else:
        input("\nInvalid Input\nPress Enter to continue....")
