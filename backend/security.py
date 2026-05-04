from dotenv import load_dotenv
import bcrypt
from cryptography.fernet import Fernet, InvalidToken
import os

# Load environment variables from .env
load_dotenv()

# Get secret key
KEY = os.getenv("SECRET_KEY")

if KEY is None:
    raise ValueError("SECRET_KEY not set in .env file")

# Initialize cipher
cipher = Fernet(KEY)


# =========================
# PASSWORD FUNCTIONS
# =========================

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed)


# =========================
# ENCRYPTION FUNCTIONS
# =========================

def encrypt_data(data: str) -> bytes:
    return cipher.encrypt(data.encode())


def decrypt_data(data) -> str:
    """
    Safely decrypt data.
    - If encrypted → decrypt
    - If plain text → return as-is
    - Never crashes
    """
    try:
        # Try decrypting (works if properly encrypted)
        return cipher.decrypt(data).decode()

    except (InvalidToken, TypeError, ValueError):
        # If it's NOT encrypted, just return it safely
        try:
            if isinstance(data, bytes):
                return data.decode(errors="ignore")
            return str(data)
        except Exception:
            return str(data)
