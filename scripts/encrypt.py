import pyDes

def encrypt_with_des(master_password, app_password):
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

    return encrypted_password_hex

