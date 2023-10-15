# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_main.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QTimer
import bcrypt

# Import the Ui_RegisterDialog class from registerdialog.py
from RegisterDialog import Ui_RegisterDialog
from SigninDialog import Ui_SigninDialog

import mysql.connector
from mysql.connector import Error


class Ui_MainWindow(object):
    def __init__(self):
        self.msg_box = None 
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(599, 473)
        MainWindow.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        MainWindow.setFont(font)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pwd_manager_label = QtWidgets.QLabel(self.centralwidget)
        self.pwd_manager_label.setGeometry(QtCore.QRect(140, 100, 321, 51))
        self.pwd_manager_label.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Baskerville Old Face")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setKerning(True)
        self.pwd_manager_label.setFont(font)
        self.pwd_manager_label.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.pwd_manager_label.setAutoFillBackground(False)
        self.pwd_manager_label.setTextFormat(QtCore.Qt.AutoText)
        self.pwd_manager_label.setScaledContents(False)
        self.pwd_manager_label.setObjectName("pwd_manager_label")
        self.register_button = QtWidgets.QPushButton(self.centralwidget)
        self.register_button.setGeometry(QtCore.QRect(200, 190, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Bookman Old Style")
        font.setPointSize(12)
        self.register_button.setFont(font)
        self.register_button.setObjectName("register_button")

        # Connect the register_button click event to open the RegisterDialog
        self.register_button.clicked.connect(self.open_register_dialog)

        self.cryptwizard_label = QtWidgets.QLabel(self.centralwidget)
        self.cryptwizard_label.setGeometry(QtCore.QRect(190, 20, 241, 51))
        font = QtGui.QFont()
        font.setFamily("High Tower Text")
        font.setPointSize(30)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.cryptwizard_label.setFont(font)
        self.cryptwizard_label.setObjectName("cryptwizard_label")
        self.sign_in_button = QtWidgets.QPushButton(self.centralwidget)
        self.sign_in_button.setGeometry(QtCore.QRect(200, 270, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Bookman Old Style")
        font.setPointSize(12)
        self.sign_in_button.setFont(font)
        self.sign_in_button.setObjectName("sign_in_button")

        # Connect the register_button click event to open the RegisterDialog
        self.sign_in_button.clicked.connect(self.open_signin_dialog)

        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setGeometry(QtCore.QRect(200, 350, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Bookman Old Style")
        font.setPointSize(12)
        self.exit_button.setFont(font)
        self.exit_button.setObjectName("exit_button")

        # Connect the exit_button click event to close the MainWindow
        self.exit_button.clicked.connect(MainWindow.close)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pwd_manager_label.setText(_translate("MainWindow", "  PASSWORD MANAGER"))
        self.register_button.setText(_translate("MainWindow", "Register"))
        self.cryptwizard_label.setText(_translate("MainWindow", "CryptWizard"))
        self.sign_in_button.setText(_translate("MainWindow", "Sign In"))
        self.exit_button.setText(_translate("MainWindow", "Exit"))

#--------------------------------------------------------------------------------------

    def open_register_dialog(self):
        register_dialog_obj.setupUi(register_dialog)
          
        # Connect the cancel_button click event to close the register_dialog
        register_dialog_obj.cancel_button.clicked.connect(self.cancel_register)
        register_dialog_obj.register_button.clicked.connect(self.register_user)
        self.exit_button.clicked.connect(register_dialog.close)        

        # Connect the checkbox state change to the toggle_echo_mode function
        register_dialog_obj.pwd_visible_checkbox.stateChanged.connect(self.pwd_checkbox_check)
        register_dialog_obj.confirm_pwd_visible_checkbox.stateChanged.connect(self.confirm_pwd_checkbox_check)

        # Show the RegisterDialog
        register_dialog.show()

    def open_signin_dialog(self):
        signin_dialog_obj.setupUi(signin_dialog)
        # Show the SigninDialog
        signin_dialog.show()
        # Connect the cancel_button click event to close the signin_dialog
        signin_dialog_obj.cancel_button.clicked.connect(self.cancel_signin)
        signin_dialog_obj.confirm_button.clicked.connect(self.signin_user)

        self.exit_button.clicked.connect(signin_dialog.close)


    def register_user(self):
        input_username = register_dialog_obj.username_input_field.text()
        input_password = register_dialog_obj.pwd_input_field.text()
        input_confirm_pwd = register_dialog_obj.confirm_pwd_input_field.text()

        cred_check, error_label = self.is_valid(input_username, "Username")
        username = ''
        if cred_check:
            register_dialog_obj.username_error_label.hide()
            username = cred_check
        elif error_label:
            register_dialog_obj.username_error_label.setText(error_label)
            register_dialog_obj.username_error_label.show()

        cred_check, error_label = self.is_valid(input_password, "Password")
        master_password = ''
        if cred_check:
            register_dialog_obj.password_error_label.hide()
            master_password = cred_check
        elif error_label:
            register_dialog_obj.password_error_label.setText(error_label)
            register_dialog_obj.password_error_label.show()

        cred_check, error_label = self.is_valid(input_confirm_pwd, "Confirm Password")
        confirm_password = ''
        if cred_check:
            register_dialog_obj.confirm_pwd_error_label.hide()
            confirm_password = cred_check
        elif error_label:
            register_dialog_obj.confirm_pwd_error_label.setText(error_label)
            register_dialog_obj.confirm_pwd_error_label.show()

        if len(username) >= 8 and len(master_password) >= 8 and len(confirm_password) != 0 :
            if confirm_password == master_password:
                # Generate a random salt
                salt = bcrypt.gensalt()        
                # Derive the master key using the master password and salt
                hashed_master_key = self.hash_master_key(master_password, salt)
                connection = self.connect_to_database()
                if connection:
                    try:
                        cursor = connection.cursor()
                        query = "INSERT INTO Users (username, salt, master_key) VALUES (%s, %s, %s)"
                        cursor.execute(query, (username, salt.decode(), hashed_master_key.decode()))
                        connection.commit()
                        self.show_message_box("Registration", "  Registration Successful  ", QMessageBox.Information)
                        register_dialog.close()
                    except Error as e:
                        self.show_message_box("Registration Error","Error in User Registration",QMessageBox.Critical)
                    finally:
                        cursor.close()
                        connection.close()
            else:
                self.show_message_box("Registration Error","Password didn't match\nRegistration failed!", QMessageBox.Critical)


    def signin_user(self):
        input_username = signin_dialog_obj.username_input_field.text()
        input_password = signin_dialog_obj.pwd_input_field.text()

        if input_username == '':
            signin_dialog_obj.username_error_label.setText("*Username required")
            signin_dialog_obj.username_error_label.show()
        else:
            signin_dialog_obj.username_error_label.hide()
        if input_password == '':
            signin_dialog_obj.password_error_label.setText("*User Password reqired")
            signin_dialog_obj.password_error_label.show()
        else:
            signin_dialog_obj.password_error_label.hide()

        if len(input_username) != 0 and len(input_password) != 0:
            connection = self.connect_to_database()
            if connection:
                try:
                    cursor = connection.cursor()
                    query1 = "SELECT id, username, salt, master_key FROM Users WHERE username = %s"
                    cursor.execute(query1, (input_username, ))
                    result = cursor.fetchone()
                    if result:
                        logged_user_id, logged_username, stored_salt, stored_master_key = result
                        # Derive the master key using the provided master password and stored salt
                        user_master_key = self.hash_master_key(input_password, stored_salt.encode())

                        if user_master_key == stored_master_key.encode():
                            
                            # Generate a salt for the Fernet key
                            #salt = os.urandom(16)

                            # Generate a Fernet key from the user's master key and the salt
                            #cipher_key = self.initialize_cipher_key(input_password, salt)
                            # Initializing cipher key with user master key
                            #cipher_key = initialize_cipher_key(user_master_key)

                            self.show_message_box("Login","Authentication successful !!!",QMessageBox.Information)
                            signin_dialog.close()
                            #return logged_user_id,logged_username,cipher_key
                        else:
                            self.show_message_box("Login Failed","Authentication failed !!!\nUsername or Password is Incorrect",QMessageBox.Critical)
                    else:
                        self.show_message_box("Login Failed", "Unrecognized User \n Authentication failed !!!", QMessageBox.Critical)
                    #sleep(0.7)
                    #return None,None,None
                    
                except Error as e:
                   self.show_message_box("Login Error","Error in User Login ", QMessageBox.Warning)
                finally:
                    cursor.close()
                    connection.close()

    def show_message_box(self, title, message, icon):
        self.msg_box = QMessageBox()
        self.msg_box.setWindowTitle(title)
        self.msg_box.setText(message)
        self.msg_box.setIcon(icon)
        self.msg_box.exec_()

    def cancel_register(self):
        register_dialog_obj.username_error_label.hide()
        register_dialog_obj.password_error_label.hide()
        register_dialog_obj.confirm_pwd_error_label.hide()
        register_dialog.close()
    def cancel_signin(self):
        signin_dialog_obj.username_error_label.hide()
        signin_dialog_obj.password_error_label.hide()
        signin_dialog.close()

    def pwd_checkbox_check(self, state):
        # Toggle the echo mode of pwd_input_field1 based on the state of show_password_checkbox1
        if state == QtCore.Qt.Checked:
            register_dialog_obj.pwd_input_field.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            register_dialog_obj.pwd_input_field.setEchoMode(QtWidgets.QLineEdit.Password)
    def confirm_pwd_checkbox_check(self, state):
        # Toggle the echo mode of pwd_input_field2 based on the state of show_password_checkbox2
        if state == QtCore.Qt.Checked:
            register_dialog_obj.confirm_pwd_input_field.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            register_dialog_obj.confirm_pwd_input_field.setEchoMode(QtWidgets.QLineEdit.Password)
        

    def is_valid(self,credential,cred_type):
        credential = credential.strip()
        if cred_type == ("Username") :
            if credential == '' :
                error_message = "*Username Required"
            elif len(credential) < 8 :
                error_message = "*Aleast 8 characters required"
            elif len(credential) > 25 :
                error_message = "*Only 25 characters allowed"
            else:
                return credential,None
            
        elif cred_type == ("Password"):
            if credential == '':
                error_message = "*User Password Required"
            elif credential.count(" ") != 0:
                error_message = "*Password can't have space"
            elif len(credential) < 8 or len(credential) > 25:
                error_message = "*Password must have 8 - 25 characters"                
            else:
                return credential, None
        
        elif cred_type == ("Confirm Password"):
            if credential == '':
                error_message = "*Please Confirm Password"
            else:
                return credential, None

        elif cred_type == ("Website") :
            if credential == '' :
                error_message = "*Website required"
            else:
                return credential,None
        return None, error_message
            
    def hash_master_key(self, master_password, salt):
        return bcrypt.hashpw(master_password.encode(), salt)

    def connect_to_database(self):
        try:
            connection = mysql.connector.connect(**self.db_config)
            if connection.is_connected():
                return connection
        except Error as e:
            self.show_message_box("Connection Error", "Can't connect to Database", QMessageBox.Critical)
            exit

    def initialize_database(self):
        self.db_config = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': 'asdf'
        }
        connection = self.connect_to_database()
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
                self.db_config['database'] = 'passwordmanager'
            except Error as e:
                self.show_message_box("Database Error", "Can't Initialize Database", QMessageBox.Critical)
                exit()
            finally:
                cursor.close()
                connection.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    main_window_obj = Ui_MainWindow()
    main_window_obj.setupUi(MainWindow)

    register_dialog = QDialog()
    register_dialog_obj = Ui_RegisterDialog()

    signin_dialog = QDialog()
    signin_dialog_obj = Ui_SigninDialog()
    
    main_window_obj.initialize_database()

    MainWindow.show()
    sys.exit(app.exec_())