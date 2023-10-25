import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

def encrypt_password(key, plaintext_password):
    formatted_key = generate_valid_key(key)
    cipher_suite = Fernet(formatted_key)
    encrypted_password = cipher_suite.encrypt(plaintext_password.encode('utf-8'))
    return encrypted_password


def generate_valid_key(key):
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    formatted_key = base64.urlsafe_b64encode(kdf.derive(key.encode('utf-8')))
    return formatted_key