# MapMyMint

## Overview
MapMyMint is a budgeting web application that helps users keep track of their spending, categories, and financial goals. It also includes a visual chart to show how money is being used.

The project was built using:
- Frontend: HTML, CSS, JavaScript (D3.js)
- Backend: Python (FastAPI)
- Database: SQLite (SQLAlchemy)

---

## Requirements

- Python 3.9+ installed  
- Repository opened in Visual Studio Code  

Install dependencies:

```bash
pip install fastapi uvicorn requests sqlalchemy pandas bcrypt cryptography python-dotenv
```

---

## Environment Setup

Create a `.env` file in the main project folder and add:

```
SECRET_KEY=your_key_here
```

To generate a key, run:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

---

## Running the Project

### Start Backend

From the main project folder, run:

```bash
uvicorn frontend.serverAPI:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

### Open Frontend (VS Code)

This project uses the **Live Preview extension by Microsoft**.

Steps:
1. Install "Live Preview" from Extensions  
2. Install on Codespace  
3. Right click `home.html`  
4. Click **Open with Live Preview**  

---

## Features

- Create and log into an account  
- Add and track transactions  
- Create budget categories  
- Track savings goals  
- View spending using a chart  
- Import and export data using CSV  

---

## Auto Testing

This project includes an automated test file:

```
Auto_Testing/automated_test.py
```

### What it tests

- User registration and login  
- Creating and retrieving categories  
- Creating and retrieving transactions  
- Creating and retrieving goals  
- Updating goal progress  
- Checking that data exists for CSV export  

### How to run

1. Start the backend:

```bash
uvicorn frontend.serverAPI:app --reload
```

2. In a new terminal, run:

```bash
python Auto_Testing/automated_test.py
```

### Output

You will see results like:

```
Testing: Register User
PASSED: Register User

Testing: Create Category
PASSED: Create Category
```

Each test shows **PASSED** or **FAILED**.

### Notes

- A new user is created each time the test runs  
- No setup data is required  
- Tests use the same API endpoints as the frontend  

---

## Manual Testing

Testing is done by interacting with the application.

### CSV Testing

Use the provided CSV files in the `Manual_Testing` folder in this order:

1. Categories CSV  
2. Transactions CSV  
3. Goals CSV  
4. Combined CSV (all data)

After each import, verify:
- Data appears correctly  
- Categories, transactions, and goals are created  
- The chart updates properly  
- No errors occur  

Also test exporting CSV to confirm it matches the input.

### Other Manual Tests

- Create a user and log in  
- Add transactions manually  
- Create and update goals  
- Verify UI and database updates  

---

## Notes

- The backend must be running before using the frontend  
- The `.env` file must be set up or the app will not start  
- Live Preview is required to properly view the frontend  
- The project runs locally

- CSV imports require the correct format (use the provided template)  
- Duplicate categories may be created if the same CSV is imported multiple times  
- The automated test requires the backend to be running before execution

## Licenses / Third Party Libraries

This project uses the following open-source tools and libraries:

- FastAPI - MIT License
- Uvicorn - BSD 3-Clause License
- Requests - Apache 2.0 License
- SQLAlchemy - MIT License
- Pandas - BSD 3-Clause License
- bcrypt - Apache 2.0 License
- cryptography - Apache 2.0 OR BSD 3-Clause License
- python-dotenv - BSD License
- Pydantic - MIT License
- D3.js - ISC License
- SQLite - Public Domain
