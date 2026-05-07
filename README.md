# MapMyMint (README Visually Best In GitHub)

## Overview
MapMyMint is a budgeting web application that helps users keep track of their spending, categories, and financial goals. It also includes a visual chart to show how money is being used.

The project was built using:
- Frontend: HTML, CSS, JavaScript (D3.js)
- Backend: Python (FastAPI)
- Database: SQLite (SQLAlchemy)

---

## Requirements

- Python 3.9+ installed  
- Visual Studio Code installed
- Repository opened in Visual Studio Code
- GitHub account connected to Visual Studio Code

## Running the Project

**How to run from GitHub Repositiory**

1. Open our GitHub Repository - https://github.com/callahank18/MapMyMint.git
2. Click on Green <> Code Button
3. Click Green Create Codespace on Main
4. Close Out Codespace Webpage that Pops Up
5. Go Back to Repository and Click the Three Dots Next to Active ...
6. Click Open in Visual Studio Code

**This is the current viable remote installation process**

## Environment Setup

**Install dependencies:**

```bash
pip install fastapi uvicorn requests sqlalchemy pandas bcrypt cryptography python-dotenv
```
---

A `.env` file is included in the main project folder.

Open the `.env` file and replace the placeholder value with your own generated secret key:

```.env
SECRET_KEY=your_generated_key_here
```

**Note: There will be a tester key in the field, please replace with your own!**

To generate personal secret key, run:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

---

### Install Live Preview (Microsoft) (VS Code)

This project uses the **Live Preview extension by Microsoft**.

Steps:
1. Install "Live Preview" from Extensions using this command, this should install the extension and apply it to the workspace.
```bash
code --install-extension ms-vscode.live-server
```    

---


### Start Backend / Frontend

From the main project folder, run:

```bash
uvicorn frontend.serverAPI:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```
2. Right click `home.html` located in frontend folder
3. Click **Open with Live Preview or Preview**
_Extend Window As You Please_
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

1. Ensure the backend is running:

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
