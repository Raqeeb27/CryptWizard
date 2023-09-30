## Import Modules
import os
from cryptography.fernet import Fernet
import getpass
from time import time, sleep

##------------------------------------------------------------------------
# Key Generation Function

def generate_key():
    try:
        key = Fernet.generate_key()    
        with open(master_key,'wb') as file :
            file.write(key)
    except:
        print("\nError in generating the Key file !!!\n")
        exit()

##------------------------------------------------------------------------
# Key Load Function

def load_key():
    try:
        with open(master_key, 'rb') as file:
            key = file.read()
        return key
    except:
        print("\nError in Loading the Key !!!\n")
        exit()

##------------------------------------------------------------------------
# User class

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.passwords = {} # Dictionary to store passwords

    def add_password(self, website, password):
        self.passwords[website] = password
        print(f"\nPassword for {website} saved successfully!")
        input("\nPress Enter to Continue....")

    def get_password(self, website):
        if website in self.passwords:
            password = self.passwords[website]
            print(f"Username: {self.username}")
            print(f"Password for {website} : {password}")
        else:
            print(f"\nNo password found for {website}")
        input("\nPress Enter to Continue....")

# Create a list to store User objects
users = []

##------------------------------------------------------------------------
# Function to check unername and password format
def is_valid(cred_type,visible = True):
    if cred_type == ("Username") :
        credential = input("\nEnter Username: ").title().strip()
        # Checking username length
        if credential == '' :
            print('Username required !!!')
            return None
        elif len(credential) < 3 or len(credential) > 15 :
            print("Only 3 - 15 characters allowed in Username")
            return None
        else:
            return credential
    elif cred_type == ("Password"):
        if visible:
            credential = input("Enter Password: ")
        else:
            credential = getpass.getpass("Enter Password: ")
        # Checking password length
        if credential == '':
            print('User Password required !!!')
            return None
        elif credential.count(" ") != 0:
            print("\nPassword can't have space!!!")
            return None
        elif len(credential) < 4 or len(credential) > 12:
            print("\nPassword must have 4 - 12 characters !!!")
            return None
        else:
            return credential

    else:
        # Checking website length
        pass

##------------------------------------------------------------------------
# Create User Function

def create_user():
    print("\n---- CREATE USER ACCOUNT ----")
    cred_check = is_valid("Username")
    if cred_check:
        username = cred_check
    else:
        return
    cred_check = is_valid("Password")
    if cred_check:
        password = cred_check
    else:
        return 
    confirm_password = input("Confirm Password: ")
    if confirm_password == password :
        user = User(username, password)
        users.append(user)
        print("\nUser created successfully!")
    else:
        print("\nPassword didn't match,\nUser account creation failed!")

##------------------------------------------------------------------------
# User Login Function 

def user_login():
    print("\n---- LOGIN USER ----")
    cred_check = is_valid("Username")
    if cred_check:
        username = cred_check
    else:
        return
    cred_check = is_valid("Password",False)
    if cred_check:
        password = cred_check
    else:
        return
    for user in users:
        if user.username == username and user.password == password:
            print("\nLogin Successfull !!!\n")
            sleep(0.8)
            return user,username
        elif user.username == username and user.password != password:
            print("Login failed !!! Invalid credentials.")
            return None
    print("\nUser doesn't exist\nPlease create your User account")
    return None

##------------------------------------------------------------------------
# Access Control

master_pwd = input("\n----- PASSWORD MANAGER -----\n\nMaster Password : ")

if master_pwd != '2023':
    print("\nACCESS DECLINED !!!\nIncorrect Master Password.\n")
    exit()

print("\nACCESS GRANTED !!!\nWelcome\n")
sleep(1)

##------------------------------------------------------------------------
## Setting up Password_Manager_Files directory

workingDirectory = os.getcwd()
manager_dir = 'Password_Manager_Files'
users_dir = 'Users'
path = os.path.join(workingDirectory, manager_dir)
users_path = os.path.join(path, users_dir)

##------------------------------------------------------------------------
# Creating output directory

try:
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(users_path):
        os.makedirs(users_path)
except:
    print(f"\nError in Creating directory\n")
    exit()

##------------------------------------------------------------------------
# Files

master_key = 'Password_Manager_Files/master_key.key'

##------------------------------------------------------------------------
# Initializing password.txt file
'''
if (not os.path.exists(passwords_file)) or os.path.getsize(passwords_file) == 0:
    try:
        with open(passwords_file, 'a') as file:
            file.write("      Website       |      Password    \n
            ------------------------------------------------------------------------------------" )
    except:
        print("\nError in Creating passwords.txt file !!!\n")
        exit()'''
    
##------------------------------------------------------------------------
# Generate Key_file

if not os.path.exists(master_key):
    generate_key()

##------------------------------------------------------------------------
# Setting up the KEY

key = load_key() + master_pwd.encode()
master_key = Fernet(key)

##------------------------------------------------------------------------
# Menu Drien User display

def user_display():
    while True:
        print(f"\n--------\n| User | --> {user_name}\n--------\n")
        print("1. Add a new password")
        print("2. Retrieve a password")
        print("3. Logout\n")

        user_choice = input(" -->  ")

        if user_choice == '1':
            website = input("\nEnter Website : ").strip()
            cred_check = is_valid("Password")
            if cred_check:
                password = cred_check
            else:
                return
            confirm_password = input("Confirm Password: ")
            if confirm_password == password :
                logged_in_user.add_password(website, password)
            else:
                print("\nPassword didn't match\nFailed to save Website and Password!")
        elif user_choice == '2':
            website = input("\nEnter website to retrieve password: ").strip()
            logged_in_user.get_password(website)

        elif user_choice == '3':
            print("\nLogout Successfull !!!")
            sleep(1)
            break
        else:
            print("\nInvalid choice. Please try again.")
            sleep(0.7)
##------------------------------------------------------------------------
# Menu Drien main display

while True:

    choice = input("\n----- PASSWORD MANAGER -----\n\n1. CREATE New User\n2. Login\n3. Exit\n\n -->  ")

    if choice == '1':
        create_user()
        input("\nPress Enter to Continue....")        
    elif choice == '2':
        logged_in_user,user_name = user_login()
        if logged_in_user:
            user_display()
            input("\nPress Enter to Continue....")
        else:
            input("\nPress Enter to Continue....")
    elif choice == '3':
        print('\n !!! THANK YOU !!!\n')
        break
    else:
        print("Invalid choice. Please try again.")
        sleep(0.7)