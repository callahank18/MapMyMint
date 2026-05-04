# MapMyMint

## Overview

MapMyMint is a budgeting web application that helps users keep track of their spending, categories, and financial goals. It also includes a visual chart to show how money is being used.

The project was built using:

* Frontend: HTML, CSS, JavaScript (D3.js)
* Backend: Python (FastAPI)
* Database: SQLite (SQLAlchemy)

---

## Requirements

Make sure Python is installed (Python 3.9+ recommended).

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

This will start the backend at:

```
http://127.0.0.1:8000
```

---

### Open Frontend (VS Code)

This project uses the **Live Preview extension by Microsoft** in Visual Studio Code.

Steps:

1. Install "Live Preview" from Extensions
2. Install on Codespace
3. Right click `home.html`
4. Click **Open with Live Preview or Preview**

---

## Features

* Create and log into an account
* Add and track transactions
* Create budget categories
* Track savings goals
* View spending using a chart
* Import and export data using CSV

---

## Manual Testing

Testing is mainly done by interacting with the application and checking that everything works correctly.

One main test we perform is using the provided CSV files. These should be imported in the following order:

1. Categories CSV
2. Transactions CSV
3. Goals CSV
4. All-in-one CSV (all 3 combined)

After each import, we verify that:

* The data appears correctly in the application
* Categories, transactions, and goals are properly created
* The chart updates based on the imported data
* No errors occur during the import process

We also test exporting the data back into a CSV file to make sure it matches what was entered.

Other manual tests include:

* Creating a user and logging in
* Adding transactions manually and checking updates
* Creating goals and updating progress
* Verifying that changes are reflected in the UI and database

---

## Notes

* The backend must be running before using the frontend
* Make sure the `.env` file is set up or the app will not start
* Live Preview is required to properly view the frontend
* The project is meant to run locally

---
