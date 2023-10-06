## Import Modules
import os
import mysql.connector
from mysql.connector import Error
from cryptography.fernet import Fernet
import getpass
from time import sleep
import bcrypt
import base64

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

##------------------------------------------------------------------------
# Function to initialize database

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
            db_config['database'] = 'passwordmanager'

        except Error as e:
            print("Error initializing database:", e)
        finally:
            cursor.close()
            connection.close()

##------------------------------------------------------------------------
# Initialize cipher key using user's master key

def initialize_cipher_key(master_key,salt):
    # Derive the key from the master password and salt using a key derivation function (KDF)
    '''kdf_key = bcrypt.kdf(
        password=master_key,
        salt=salt,
        desired_key_bytes=32,  # Fernet key length is 32 bytes
        rounds=100000,  # You can adjust the number of rounds for your security needs
        #algorithm="sha256"
    )
    return Fernet(base64.urlsafe_b64encode(kdf_key))'''
##------------------------------------------------------------------------
# Function to store password for a user to the database

def record_password(user_id, website, password):
    # Encrypt the password using cipher key
    #encrypted_password = cipher_key.encrypt(password)
    #print(type(encrypted_password))
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO Passwords (user_id, website, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (user_id, website, password))
            connection.commit()
            print(f"\nPassword for '{website}' saved successfully!")
            input("\nPress Enter to Continue....")

        except Error as e:
            print("Error adding password:", e)
        finally:
            cursor.close()
            connection.close()
    
##------------------------------------------------------------------------
# Function to retrieve password for a user from the database

def lookup_password(user_id, username, website):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT password FROM Passwords WHERE user_id = %s AND website = %s"
            cursor.execute(query, (user_id, website))
            result = cursor.fetchone()
            if result:
                password = result[0]
                # Decrypt the password
                #decrypted_password = cipher_key.decrypt(encrypted_password.encode()).decode()
                print(f"\nUsername: {username}")
                print(f"Password for '{website}' : {password}")
            else:
                print(f"\nNo password found for '{website}'")
            input("\nPress Enter to Continue....")

        except Error as e:
            print("Error retrieving password:", e)
        finally:
            cursor.close()
            connection.close()

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
        
##------------------------------------------------------------------------
# Function to create Hash of User Master key

def hash_master_key(master_password, salt):
    return bcrypt.hashpw(master_password.encode(), salt)

##------------------------------------------------------------------------
# Create User Function

def register_user():
    print("\n------ CREATE USER ACCOUNT ------")
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
                cursor.execute(query, (username, salt.decode(), hashed_master_key.decode()))
                connection.commit()
                print("\nUser created successfully!")
            except Error as e:
                print(f"Error creating User Account: {e}\n")
            finally:
                cursor.close()
                connection.close()
    else:
        print("\nPassword didn't match,\nUser account creation failed!")

##------------------------------------------------------------------------
# User Login Function 

def user_login():
    print("\n------ USER LOGIN ------")
    cred_check = is_valid("Username")
    if cred_check:
        username = cred_check
    else:
        return None,None,None
    cred_check = is_valid("Password",False)
    if cred_check:
        input_password = cred_check
    else:
        return None,None,None
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            query1 = "SELECT id, username, salt, master_key FROM Users WHERE username = %s"
            cursor.execute(query1, (username, ))
            result = cursor.fetchone()
            if result:
                logged_user_id, logged_username, stored_salt, stored_master_key = result
                # Derive the master key using the provided master password and stored salt
                user_master_key = hash_master_key(input_password, stored_salt.encode())

                if user_master_key == stored_master_key.encode():
                    print("\nAuthentication successful !!!\n")
                    # Generate a salt for the Fernet key
                    salt = os.urandom(16)

                    # Generate a Fernet key from the user's master key and the salt
                    cipher_key = initialize_cipher_key(input_password, salt)
                    # Initializing cipher key with user master key
                    #cipher_key = initialize_cipher_key(user_master_key)
                    #print(type(cipher_key))

                    sleep(1)
                    return logged_user_id,logged_username,cipher_key
                else:
                    print("\nAuthentication failed !!!\nUsername or Password is Incorrect\n")
            else:
                print("\n Unrecognized User - Authentication failed !!!")
            sleep(0.7)
            return None,None,None
            
        except Error as e:
            print("Error in User Login: ", e)
        finally:
            cursor.close()
            connection.close()

##------------------------------------------------------------------------
# Menu Drien Logged in User display

def logged_user_display():
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
                record_password(logged_user_id,website, password)
            else:
                print("\nPassword didn't match\nFailed to save Website and Password!")

        elif user_choice == '2':
            cred_check = is_valid("Website")
            if cred_check:
                website = cred_check
            else:
                return
            lookup_password(logged_user_id,logged_username,website)

        elif user_choice == '3':
            print("\nLogout Successfull !!!")
            sleep(1)
            break
        else:
            print("\nInvalid choice. Please try again.")
            sleep(0.7)
##------------------------------------------------------------------------
# Menu Drien main display

initialize_database()

while True:

    print("\n----------------------------------\n  --------- CryptWizard --------\n   ----- PASSWORD MANAGER -----\n")
    choice = input("1. Register\n2. Login\n3. Exit\n\n -->  ")
    if choice == '1':
        register_user()
        input("\nPress Enter to Continue....")        
    elif choice == '2':
        logged_user_id, logged_username, cipher_key = user_login()
        if logged_user_id:
            logged_user_display()
            input("\nPress Enter to Continue....")
        else:
            input("\nPress Enter to Continue....")
    elif choice == '3':
        print("\n!!! Thank You !!!\n")
        sleep(0.6)
        print('\n ---------- CryptWizard -----------\n\n Your security is our top priority.\n\t Have a great day!\n\n')
        break
    else:
        print("Invalid choice. Please try again.")
        sleep(0.7)