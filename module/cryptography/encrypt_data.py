# Encrypt the data
import json
from cryptography.fernet import Fernet


def encrypt_data(key: bytes, data: dict) -> str:
    fernet = Fernet(key)
    # Convert data to string use json
    data = json.dumps(data)
    encrypted_data = fernet.encrypt(data.encode())
    return f"{encrypted_data.decode()}.{key.decode()}"
