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
        self.passwords = {}  # Dictionary to store passwords


# Create a list to store User objects
users = []

##------------------------------------------------------------------------
# Create User Function

def create_user():
    username = input("\nEnter Username: ").title()
    password = getpass.getpass("Enter Password: ")
    confirm_password = getpass.getpass("Confirm Password: ")
    if confirm_password == password :
        user = User(username, password)
        users.append(user)
        print("\nUser created successfully!")
    else:
        print("\nPassword didn't match,\nUser account creation failed!")

##------------------------------------------------------------------------
# User Login Function 

def user_login():
    username = input("\nUsername: ").title()
    password = getpass.getpass("Password: ")
    for user in users:
        if user.username == username and user.password == password:
            print("Login Successfull !!!")
            return username
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
        print(f"\nUser : {logged_in_user}\n")
        print("1. Add a new password")
        print("2. Retrieve a password")
        print("3. Logout")

        user_choice = input("Enter your choice: ")

        if user_choice == '1':
            website = input("Enter website: ")
            password = getpass.getpass("Enter password: ")
            logged_in_user.add_password(website, password)
        elif user_choice == '2':
            website = input("Enter website to retrieve password: ")
            logged_in_user.get_password(website)
        elif user_choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")
##------------------------------------------------------------------------
# Menu Drien main display

while True:

    choice = input("\n----- PASSWORD MANAGER -----\n\n1. CREATE New User\n2. Login\n3. Exit\n\n -->  ")

    if choice == '1':
        create_user()
        input("\nPress Enter to Continue....")        
    elif choice == '2':
        logged_in_user = user_login()
        if logged_in_user:
            user_display()
        else:
            input("\nPress Enter to Continue....")
    elif choice == '3':
        print('\n !!! THANK YOU !!!\n')
        break
    else:
        print("Invalid choice. Please try again.")
        sleep(0.7)