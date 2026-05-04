# MapMyMint

MapMyMint is a full-stack budgeting application that helps users track spending, visualize financial data, and manage savings goals. It includes a FastAPI backend, SQLite database & SQLalchemy library, and a dynamic frontend dashboard.

## Features
- User account creation and login (secure password hashing)
- Encrypted storage of sensitive data (goals, transactions)
- Budget tracking and visualization
- Goal management system
- REST API built with FastAPI

  
## Security Features
- Passwords are hashed using bcrypt
- Sensitive data is encrypted using Fernet (cryptography library)
- Secret key stored securely using environment variables (.env)
- System supports both encrypted and legacy plaintext data safely

## Codespace/Software Used
Visual Studio Code
(Codespaces via Github was causing multiple errors!)

## Installation
1. Clone the repository:
```bash
git clone https://github.com/your-repo/MapMyMint.git
cd MapMyMint


## Dependencies
pip install sqlalchemy pandas bcrypt cryptography python-dotenv fastapi uvicorn pydanticp


##Environment Setup (.env)
Create a `.env` file in the root directory and add:
SECRET_KEY=your_generated_key_here


##To generate a key:
from cryptography.fernet import Fernet
print(Fernet.generate_key())


## Running the Backend
Start the FastAPI server:
```bash
uvicorn frontend.serverAPI:app --reload

## Auto Test
```bash
pytest



