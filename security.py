import bcrypt
from cryptography.fernet import Fernet
import os

KEY = os.getenv("SECRET_KEY")

if KEY is None:
    raise ValueError("SECRET_KEY not set")

cipher = Fernet(KEY)

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed)

def encrypt_data(data: str) -> bytes:
    return cipher.encrypt(data.encode())

def decrypt_data(data: bytes) -> str:
    return cipher.decrypt(data).decode()
