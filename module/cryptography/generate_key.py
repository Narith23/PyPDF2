from cryptography.fernet import Fernet


# Generate a key for encryption
def generate_key():
    key = Fernet.generate_key()
    return key
