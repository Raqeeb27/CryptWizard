## Import Modules
import mysql.connector
from mysql.connector import Error
import os
from cryptography.fernet import Fernet
import getpass
from time import time, sleep
import bcrypt

##------------------------------------------------------------------------
# Function to establish a database connection

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'asdf'
}

def connect_to_database():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print("\nError connecting to the database:", e)
    return None

def initialize_database():
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Create the database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS passwordmanager")
            cursor.execute("USE passwordmanager")

            # Create the Users table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    salt CHAR(29) NOT NULL,
                    master_key VARCHAR(255) NOT NULL
                )
            """)

            # Create the Passwords table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Passwords (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    website VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES Users(id)
                )
            """)

            connection.commit()
            cursor.close()
            connection.close()
            db_config['database'] = 'passwordmanager'
        except Error as e:
            print("Error initializing database:", e)

initialize_database()

'''##------------------------------------------------------------------------
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
'''
##------------------------------------------------------------------------
# 

def add_password(user_id, website, password):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO Passwords (user_id, website, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (user_id, website, password))
            connection.commit()
            cursor.close()
            connection.close()
            print(f"\nPassword for '{website}' saved successfully!")
            input("\nPress Enter to Continue....")
        except Error as e:
            print("Error adding password:", e)
    
# Function to retrieve a password for a user from the database
def get_password(user_id, username, website):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT password FROM Passwords WHERE user_id = %s AND website = %s"
            cursor.execute(query, (user_id, website))
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            if result:
                print(f"\nUsername: {username}")
                print(f"Password for '{website}' : {result[0]}")
            else:
                print(f"\nNo password found for '{website}'")
            input("\nPress Enter to Continue....")
        except Error as e:
            print("Error retrieving password:", e)
'''
    if website in passwords:
        password = passwords[website]
        print(f"Username: {username}")
        print(f"Password for {website} : {password}")
    else:
        print(f"\nNo password found for {website}")
    input("\nPress Enter to Continue....")
    '''


##------------------------------------------------------------------------
# Function to check unername and password format
def is_valid(cred_type,visible = True):
    if cred_type == ("Username") :
        credential = input("\nEnter Username : ").title().strip()
        # Checking username length
        if credential == '' :
            print('Username required !!!')
            return None
        elif len(credential) < 3 or len(credential) > 25 :
            print("Only 3 - 25 characters allowed in Username")
            return None
        else:
            return credential
        
    elif cred_type == ("Password"):
        if visible:
            credential = input("Enter Password : ")
        else:
            credential = getpass.getpass("Enter Password : ")
        # Checking password length
        if credential == '':
            print('User Password required !!!')
            return None
        elif credential.count(" ") != 0:
            print("\nPassword can't have space!!!")
            return None
        elif len(credential) < 4 or len(credential) > 25:
            print("\nPassword must have 4 - 25 characters !!!")
            return None
        else:
            return credential

    elif cred_type == ("Website") :
        credential = input("\nEnter Website : ").strip()
        # Checking website length
        if credential == '' :
            print('Website required !!!')
            return None
        else:
            return credential

def hash_master_key(master_password, salt):
    return bcrypt.hashpw(master_password.encode('utf-8'), salt)


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
        master_password = cred_check
    else:
        return 
    confirm_password = input("Confirm Password: ")
    if confirm_password == master_password :
        
        # Generate a random salt
        salt = bcrypt.gensalt()
        
        # Derive the master key using the master password and salt
        hashed_master_key = hash_master_key(master_password, salt)

        connection = connect_to_database()
        if connection:
            try:
                cursor = connection.cursor()
                query = "INSERT INTO Users (username, salt, master_key) VALUES (%s, %s, %s)"
                cursor.execute(query, (username, salt, hashed_master_key))
                connection.commit()
                cursor.close()
                connection.close()
                print("\nUser created successfully!")
            except Error as e:
                print(f"Error creating User Account: {e}\n")
    else:
        print("\nPassword didn't match,\nUser account creation failed!")

##------------------------------------------------------------------------
# User Login Function 

def user_login():
    print("\n---- USER LOGIN ----")
    cred_check = is_valid("Username")
    if cred_check:
        username = cred_check
    else:
        return None,None
    cred_check = is_valid("Password",False)
    if cred_check:
        input_password = cred_check
    else:
        return None,None
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            query1 = "SELECT id, username, salt, master_key FROM Users WHERE username = %s"
            cursor.execute(query1, (username, ))
            result = cursor.fetchone()
            if result:
                logged_user_id, logged_username, stored_salt, stored_master_key = result
                #2
                # print("logged_user_id = "+logged_user_id)
                print("logged_username = "+logged_username)
                print("stored_salt = "+stored_salt)
                print("stored_master_key = "+stored_master_key)

                # Derive the master key using the provided master password and stored salt
                input_master_key = hash_master_key(input_password, stored_salt)
                print("input_master_key = "+input_master_key)

                if input_master_key == stored_master_key:
                    print("Authentication successful !!!")
                    # Use input_master_key to decrypt user data
                    sleep(1)
                    return logged_user_id,logged_username
                else:
                    print("Authentication failed !!!\nUsername or Password is Incorrect\n")
            else:
                print("Unrecognized User. Authentication failed !!!")
                '''print("\nLogin Successfull !!!")
                sleep(1)
                return result_id[0],username
            cursor = connection.cursor()
            query2 = "SELECT id FROM Users WHERE username = %s"
            cursor.execute(query2, (username,))
            result_user = cursor.fetchone()       
            if result_user:
                print("\nLogin failed !!! Invalid credentials.")
                return None,None
            else:
                print("\nUser doesn't exist\nPlease create your User account")'''
                return None,None
            
        except Error as e:
            print("Error in User Login: ", e)
        finally:
            cursor.close()
            connection.close()

'''
##------------------------------------------------------------------------
# Access Control

master_pwd = input("\n----- PASSWORD MANAGER -----\n\nMaster Password : ")

if master_pwd != '2023':
    print("\nACCESS DECLINED !!!\nIncorrect Master Password.\n")
    exit()

print("\nACCESS GRANTED !!!\nWelcome\n")
sleep(1)


##------------------------------------------------------------------------
## Setting up passwordmanager_Files directory

workingDirectory = os.getcwd()
manager_dir = 'passwordmanager_Files'
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

master_key = 'passwordmanager_Files/master_key.key'

##------------------------------------------------------------------------
# Initializing password.txt file

if (not os.path.exists(passwords_file)) or os.path.getsize(passwords_file) == 0:
    try:
        with open(passwords_file, 'a') as file:
            file.write("      Website       |      Password    \n
            ------------------------------------------------------------------------------------" )
    except:
        print("\nError in Creating passwords.txt file !!!\n")
        exit()
    
##------------------------------------------------------------------------
# Generate Key_file

if not os.path.exists(master_key):
    generate_key()

##------------------------------------------------------------------------
# Setting up the KEY

key = load_key() + master_pwd.encode()
master_key = Fernet(key)
'''
##------------------------------------------------------------------------
# Menu Drien User display

def user_display():
    while True:
        print(f"\n--------\n| User | --> {logged_username}\n--------\n")
        print("1. New Password Record")
        print("2. Retrieve password")
        print("3. Logout\n")

        user_choice = input(" -->  ")

        if user_choice == '1':
            cred_check = is_valid("Website")
            if cred_check:
                website = cred_check
            else:
                return
            
            cred_check = is_valid("Password")
            if cred_check:
                password = cred_check
            else:
                return
            confirm_password = input("Confirm Password: ")
            if confirm_password == password :
                add_password(logged_user_id,website, password)
            else:
                print("\nPassword didn't match\nFailed to save Website and Password!")
        elif user_choice == '2':
            cred_check = is_valid("Website")
            if cred_check:
                website = cred_check
            else:
                return
            get_password(logged_user_id,logged_username,website)

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

    choice = input("\n----- PASSWORD MANAGER -----\n\n1. Register\n2. Login\n3. Exit\n\n -->  ")

    if choice == '1':
        create_user()
        input("\nPress Enter to Continue....")        
    elif choice == '2':
        logged_user_id,logged_username = user_login()
        if logged_user_id:
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