import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton
import pyDes
import hashlib

def encrypt_with_des(master_password, app_password):
    # Ensure the master password is 8 bytes long (or pad it if it's shorter)
    master_password = master_password.ljust(8, '\0')[:8]

    # Convert the master password to bytes
    master_password_bytes = master_password.encode('utf-8')

    # Create a DES object with the master password as the key
    des = pyDes.des(master_password_bytes, pyDes.ECB, pad=None, padmode=pyDes.PAD_PKCS5)

    # Convert the application password to bytes
    app_password_bytes = app_password.encode('utf-8')

    # Encrypt the application password
    encrypted_password = des.encrypt(app_password_bytes)

    # Convert the encrypted password bytes to a hexadecimal representation
    encrypted_password_hex = encrypted_password.hex()

    print(encrypted_password,encrypted_password_hex)
    return encrypted_password_hex


# Import the encrypt_with_des function here...

class PasswordManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Password Manager")

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Create QLabel and QLineEdit for the master password
        master_password_label = QLabel("Master Password:")
        self.master_password_input = QLineEdit()
        main_layout.addWidget(master_password_label)
        main_layout.addWidget(self.master_password_input)

        # Create QLabel and QLineEdit for the application password
        app_password_label = QLabel("Application Password:")
        self.app_password_input = QLineEdit()
        main_layout.addWidget(app_password_label)
        main_layout.addWidget(self.app_password_input)

        # Create a QPushButton to perform the encryption
        encrypt_button = QPushButton("Encrypt")
        encrypt_button.clicked.connect(self.encrypt_password)
        main_layout.addWidget(encrypt_button)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def encrypt_password(self):
        master_password = self.master_password_input.text()
        app_password = self.app_password_input.text()

        if master_password and app_password:
            encrypted_password = encrypt_with_des(master_password, app_password)
            # You can now do something with the encrypted password, e.g., store it in your database or display it.

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PasswordManagerApp()
    window.show()
    sys.exit(app.exec_())

