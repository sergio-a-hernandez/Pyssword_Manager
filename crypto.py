import base64, os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Load or create a salt for key derivation
def load_salt(filepath="salt.bin"):
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            return f.read()
    else:
        salt = os.urandom(16)
        with open(filepath, "wb") as f:
            f.write(salt)
        return salt

# Derive a key from the password and salt using PBKDF2
def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

# Get a Fernet instance using the derived key
def get_fernet(password):
    salt = load_salt()
    key = derive_key(password, salt)
    return Fernet(key)
