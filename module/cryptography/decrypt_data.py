# Decrypt the data
from datetime import datetime
from cryptography.fernet import Fernet
import json


def decrypt_data(encrypted_data: str) -> dict:
    key = encrypted_data.split(".")[1]
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()

    # Json loads
    decrypted_data = json.loads(decrypted_data)

    # Convert expiration_date (which is a Unix timestamp) back to datetime object
    expiration_date = datetime.fromtimestamp(decrypted_data["expiration_date"])

    # Check if expiration_date is in the past
    current_time = datetime.now()
    if expiration_date < current_time:
        return "The data has expired."

    return decrypted_data
