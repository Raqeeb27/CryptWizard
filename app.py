import sys
import bcrypt
import mysql.connector
from mysql.connector import Error
from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QDialog, QLineEdit, QMessageBox, QHBoxLayout

app = QApplication(sys.argv)

class LoggedinDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Login")
        self.setGeometry(400, 180, 500, 450)
        self.register_window = RegistrationDialog()

        self.initUI()

    def initUI(self):

        layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()

        layout.addSpacing(10)

        self.dashboard_label = QLabel("PASSWORD MANAGER DASHBOARD", self)
        self.dashboard_label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(self.dashboard_label)

        layout.addSpacing(15)

        self.welcome_label = QLabel("Welcome, {User's Name}!", self)
        self.welcome_label.setAlignment(Qt.AlignLeft)  
        horizontal_layout.addWidget(self.welcome_label)

        self.secritylevel_label = QLabel("Security Level: High  ", self)
        self.secritylevel_label.setAlignment(Qt.AlignRight)  
        horizontal_layout.addWidget(self.secritylevel_label)

        layout.addLayout(horizontal_layout)
        layout.addSpacing(20)

        self.summary_label = QLabel("Dashboard Summary:", self)
        self.summary_label.setAlignment(Qt.AlignLeft)  
        layout.addWidget(self.summary_label)

        layout.addSpacing(1)

        self.total_pwds_label = QLabel("- Total Passwords: { X}", self)
        self.total_pwds_label.setAlignment(Qt.AlignLeft)  
        layout.addWidget(self.total_pwds_label)
        layout.addSpacing(1)

        self.recent_act_label = QLabel("- Recent Activity: { Z}", self)
        self.recent_act_label.setAlignment(Qt.AlignLeft)  
        layout.addWidget(self.recent_act_label)

        layout.addSpacing(20)

        self.pwd_vault_label = QLabel("Password Vault:", self)
        self.pwd_vault_label.setAlignment(Qt.AlignLeft)  
        layout.addWidget(self.pwd_vault_label)

        layout.addStretch()

        self.setLayout(layout)

# -----------------------------------------------------------------------------------------

class LoginDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(500, 280, 300, 250)
        self.register_window = RegistrationDialog()

        self.initUI()

    def initUI(self):

        layout = QVBoxLayout()

        self.username_label = QLabel("Username", self)
        self.username_input = QLineEdit(self)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.pwd_label = QLabel("Password", self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.pwd_label)
        layout.addWidget(self.password_input)


        self.email_label = QLabel("Email", self)
        self.email_input = QLineEdit(self)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)

        self.login_button = QPushButton("Login", self)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        self.login_button.clicked.connect(self.loginAction)

    def loginAction(self):

        username = self.username_input.text()
        password = self.password_input.text()
        email = self.email_input.text()

        if not username or not password or not email:
            QMessageBox.warning(self, "Login Error", "Please fill in all fields.")
        else:
            connection = self.register_window.main_window.connect_to_database()
            if connection:
                try:
                    cursor = connection.cursor()
                    query1 = "SELECT id, username, salt, master_key FROM Users WHERE username = %s"
                    cursor.execute(query1, (username, ))
                    result = cursor.fetchone()
                    if result:
                        logged_user_id, logged_username, stored_salt, stored_master_key = result
                        # Derive the master key using the provided master password and stored salt
                        user_master_key = self.register_window.hash_master_key(password, stored_salt.encode())

                        if user_master_key == stored_master_key.encode():
                            QMessageBox.information(self, "Login Successful", "Login was successful!")
                            self.accept()
                            loggedin_dialog = LoggedinDialog()
                            loggedin_dialog.exec_()
                            # Close the registration dialog
                            #self.accept()
                            # Generate a salt for the Fernet key
                            #salt = os.urandom(16)

                            # Generate a Fernet key from the user's master key and the salt
                            #cipher_key = initialize_cipher_key(input_password, salt)
                            # Initializing cipher key with user master key
                            #cipher_key = initialize_cipher_key(user_master_key)
                            #print(type(cipher_key))

                        else:
                            QMessageBox.warning(self, "Login Error", "Authentication failed, Username or Password is Incorrect !!!")
                    else:
                        QMessageBox.warning(self, "Login Error", "Unrecognized User - Authentication failed !!!")
                    
                    
                except Error as e:
                    QMessageBox.warning(self, "Login Error", "Error in User Login")
                finally:
                    cursor.close()
                    connection.close()

# -----------------------------------------------------------------------------------------

class RegistrationDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Registration")
        self.setGeometry(500, 280, 300, 250)
        self.main_window = MyWindow()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.username_label = QLabel("Username", self)
        self.username_input = QLineEdit(self)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.pwd_label = QLabel("Password", self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.pwd_label)
        layout.addWidget(self.password_input)

        self.confirm_pwd_label = QLabel("Confirm Password", self)
        self.confirm_pwd_input = QLineEdit(self)
        self.confirm_pwd_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_pwd_label)
        layout.addWidget(self.confirm_pwd_input)

        self.email_label = QLabel("Email", self)
        self.email_input = QLineEdit(self)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)

        self.register_button = QPushButton("Register", self)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

        self.register_button.clicked.connect(self.registrationAction)


    def registrationAction(self):

        username = self.username_input.text()
        password = self.password_input.text()
        confirm_pwd = self.confirm_pwd_input.text()
        email = self.email_input.text()

        if not username or not password or not email:
            QMessageBox.warning(self, "Registration Error", "Please fill in all fields.")

        elif password != confirm_pwd:
            QMessageBox.warning(self, "Registration Error", "Input Passwords correctly !")
        
        else:

            salt = bcrypt.gensalt()        

            hashed_master_key = self.hash_master_key(password, salt)
            
            connection = self.main_window.connect_to_database()
            if connection:
                try:
                    cursor = connection.cursor()
                    query = "INSERT INTO Users (username, email, salt, master_key) VALUES (%s, %s, %s, %s)"
                    cursor.execute(query, (username, email, salt.decode(), hashed_master_key.decode()))
                    connection.commit()
                    # Show a message box indicating successful registration
                    QMessageBox.information(self, "Registration Successful", "Registration was successful!")

                    # Close the registration dialog
                    self.accept()
                except Error as e:
                    QMessageBox.warning(self, "Registration Error", "Error in User Registration")
                finally:
                    cursor.close()
                    connection.close()


    def hash_master_key(self,master_password, salt):
        return bcrypt.hashpw(master_password.encode(), salt)

# -----------------------------------------------------------------------------------------

class MyWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.db_config = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': 'asdf'
        }
        self.setWindowTitle("CryptWizard - Password Manager")
        self.setGeometry(450, 250, 400, 300)

        self.initUI()


    def connect_to_database(self):
        try:
            connection = mysql.connector.connect(**self.db_config)
            if connection.is_connected():
                return connection
        except Error as e:
            QMessageBox.warning(self, "Connection Error", "Can't connect to Database")


    def initialize_database(self):
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
                        email VARCHAR(20) NOT NULL,
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
                QMessageBox.warning(self, "Connection Error", "Can't connect to Database")
            finally:
                cursor.close()
                connection.close()

    def initUI(self):
        self.initialize_database()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        layout.addSpacing(10)

        self.pwd_manager_label = QLabel("PASSWORD MANAGER", self)
        layout.addWidget(self.pwd_manager_label)

        layout.addSpacing(20)  # Increase spacing between label and buttons

        self.register_button = QPushButton("Register", self)
        self.register_button.setFixedSize(80, 30)
        layout.addWidget(self.register_button)

        self.login_button = QPushButton("Login", self)
        self.login_button.setFixedSize(80, 30)
        layout.addWidget(self.login_button)

        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setFixedSize(80, 30)
        layout.addWidget(self.exit_button)

        layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.setSpacing(10)  # Set spacing between widgets to 10 pixels

        layout.addStretch()

        self.register_button.clicked.connect(self.showRegistrationDialog)
        self.login_button.clicked.connect(self.showloginDialog)
        self.exit_button.clicked.connect(self.closeApplication)

        central_widget.setLayout(layout)

    def showRegistrationDialog(self):
        registration_dialog = RegistrationDialog()
        registration_dialog.exec_()

    def showloginDialog(self):
        login_dialog = LoginDialog()
        login_dialog.exec_()

    def closeApplication(self):
        self.close()


window = MyWindow()
window.show()

sys.exit(app.exec_())
