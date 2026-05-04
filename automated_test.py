import requests
import time

BASE_URL = "http://127.0.0.1:8000"

print("\nStarting Tests...\n")

# make new user so it doesn't break
username = "testuser_" + str(int(time.time()))
password = "testpass123"

# register user
print("Testing: Register User")

res = requests.post(BASE_URL + "/register/", json={
    "username": username,
    "password": password
})

if res.status_code == 200:
    print("PASSED: Register User")
    user_id = res.json().get("user_id")
else:
    print("FAILED: Register User")
    user_id = None

# login user
print("\nTesting: Login User")

res = requests.post(BASE_URL + "/login/", json={
    "username": username,
    "password": password
})

if res.status_code == 200:
    print("PASSED: Login User")
else:
    print("FAILED: Login User")

# create category
print("\nTesting: Create Category")

res = requests.post(BASE_URL + "/categories/", json={
    "user_id": user_id,
    "name": "Groceries",
    "limit_amount": 400,
    "parent_category_id": None
})

if res.status_code == 200:
    print("PASSED: Create Category")
else:
    print("FAILED: Create Category")

# get categories
print("\nTesting: Get Categories")

res = requests.get(BASE_URL + f"/categories/{user_id}")
categories = res.json()

if res.status_code == 200 and any(c["name"] == "Groceries" for c in categories):
    print("PASSED: Get Categories")
else:
    print("FAILED: Get Categories")

category_id = None
for c in categories:
    if c["name"] == "Groceries":
        category_id = c["id"]

# create transaction
print("\nTesting: Create Transaction")

res = requests.post(BASE_URL + "/transactions/", json={
    "user_id": user_id,
    "category_id": category_id,
    "transaction_date": "2026-04-19",
    "description": "Walmart trip",
    "amount": 82.43,
    "transaction_type": "expense"
})

if res.status_code == 200:
    print("PASSED: Create Transaction")
else:
    print("FAILED: Create Transaction")

# get transactions
print("\nTesting: Get Transactions")

res = requests.get(BASE_URL + f"/transactions/{user_id}")
transactions = res.json()

if res.status_code == 200 and any(t["description"] == "Walmart trip" for t in transactions):
    print("PASSED: Get Transactions")
else:
    print("FAILED: Get Transactions")

# create goal
print("\nTesting: Create Goal")

res = requests.post(BASE_URL + "/goals/", json={
    "user_id": user_id,
    "goal_name": "Emergency Fund",
    "target_amount": 2000,
    "current_amount": 0
})

if res.status_code == 200:
    print("PASSED: Create Goal")
else:
    print("FAILED: Create Goal")

# get goals
print("\nTesting: Get Goals")

res = requests.get(BASE_URL + f"/goals/{user_id}")
goals = res.json()

if res.status_code == 200 and any("Emergency Fund" in g["goal_name"] for g in goals):
    print("PASSED: Get Goals")
else:
    print("FAILED: Get Goals")

goal_id = None
for g in goals:
    if "Emergency Fund" in g["goal_name"]:
        goal_id = g["goal_id"]

# update goal
print("\nTesting: Update Goal")

res = requests.put(BASE_URL + f"/goals/{goal_id}", json={
    "current_amount": 500
})

if res.status_code == 200:
    print("PASSED: Update Goal")
else:
    print("FAILED: Update Goal")

# check update worked
print("\nTesting: Check Goal Update")

res = requests.get(BASE_URL + f"/goals/{user_id}")
updated_goals = res.json()

if any(g["goal_id"] == goal_id and g["current_amount"] == 500 for g in updated_goals):
    print("PASSED: Goal Updated")
else:
    print("FAILED: Goal Not Updated")

# final check for csv data
print("\nTesting: Data for CSV")

if len(categories) > 0 and len(transactions) > 0 and len(goals) > 0:
    print("PASSED: Data exists")
else:
    print("FAILED: Missing data")

print("\nDone.\n")
