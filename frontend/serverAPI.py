import sys
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
# Add the parent directory to the system path to allow imports from the backend directory
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.data_service import( create_goal as create_goal_logic,
create_transaction as create_tx_logic,
get_goals,
login_user,
create_user,
update_goal_amount,
create_category,
get_categories,
get_transactions_with_names
)

from backend.models import Transaction
from typing import Optional


from backend.models import SessionLocal, Goals #Intending on taking the existing data setup and working with it

app = FastAPI()

# Set up CORS middleware to allow requests from the frontend
app.add_middleware(
     CORSMiddleware,
     allow_origins=["*"], #Allowing any origins for now, restrict as we leave testing
     allow_methods=["*"],
     allow_headers=["*"],
)

#It is my understanding that I need some manner of schema here to satisfy the need for getting response from the front end for the database querry.
#These create a schema to tell pydantic how to read in JSON files. 

class TransactionCreate(BaseModel):
    user_id: int
    category_id: Optional[int] = None  # Optional if category is a name string
    transaction_date: str
    description: str
    amount: float
    transaction_type: str = "expense" # Default to expense

class GoalCreate(BaseModel):
     user_id: int
     goal_name: str
     target_amount: float
     current_amount: float

class CategoryCreate(BaseModel):
    user_id: int
    name: str
    limit_amount: float = 0
    parent_category_id: Optional[int] = None

class GoalUpdate(BaseModel):
     current_amount: float

class LoginSchema(BaseModel):
    username: str
    password: str


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/login/")
def retrieveLogin(user: LoginSchema):
    print(user.username)
    print(user.password)
    result = login_user(user.username, user.password)
    if result["status"] == "login_error":
        raise HTTPException(status_code=401, detail=result["reason"])
    elif result["status"] == "db_error":
        raise HTTPException(status_code=500, detail=result["reason"])
    else:
        result["username"] = user.username
        return result
    

@app.post("/register/")
def createUser(user: LoginSchema):
    result = create_user(user.username, user.password)
    if result["status"] == "register_error":
        raise HTTPException(status_code=409, detail=result["reason"])
    elif result["status"] == "db_error":         
        raise HTTPException(status_code=500, detail=result["reason"])
    else:
        
        return result

@app.post("/categories/")
def create_category_route(cat: CategoryCreate):
    result = create_category(
        user_id=cat.user_id,
        name=cat.name,
        limit_amount=cat.limit_amount,
        parent_id=cat.parent_category_id
    )
    if result.get("status") == "db_error":
        raise HTTPException(status_code=500, detail=result["reason"])
    return result

@app.get("/goals/{user_id}")
def read_goals(user_id: int):
    #the intention here is to use the existing SQLalchemy setup.
    #The intent is to query the Goals table for all goals associated with the given user_id and return them as a response.
    print("userid:", user_id)
    return get_goals(user_id)

@app.get("/categories/{user_id}")
def read_categories(user_id: int):
    return get_categories(user_id)

@app.get("/transactions/{user_id}")
def read_transactions(user_id: int):
    return get_transactions_with_names(user_id)

@app.post("/goals/")
def create_goal(goal: GoalCreate):
    try:
        # We call the logic function from data_service.py
        # It handles the encryption of goal_name for us
        result = create_goal_logic(
            user_id=goal.user_id,
            goal_name=goal.goal_name,
            target_amount=goal.target_amount
        )
        
        # If your data_service version returns the new ID, pass it along
        return {"status": "success", "data": result}
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to create encrypted goal: {str(e)}"
        )

@app.post("/transactions/")
def create_transaction(item: TransactionCreate):
    # call transaction logic in data_service.py
    result = create_tx_logic(
        user_id=item.user_id,
        description=item.description,
        amount=item.amount,
        category_id=item.category_id,
        date=item.transaction_date,
        t_type=item.transaction_type
    )
    if result["status"] == "db_error":
        raise HTTPException(status_code=500, detail=result["reason"])
    return result

@app.put("/goals/{goal_id}")
def update_goal(goal_id: int, goal_update: GoalUpdate):
    result = update_goal_amount(goal_id, goal_update.current_amount)
    if result["status"] != "success":
        raise HTTPException(status_code=400, detail=result.get("reason", "error"))
    return result

# @app.delete("/goals/{user_id}")
#def delete_goals(user_id: int):
#    db = SessionLocal()
#    try:
#       db.query(Goals).filter(Goals.user_id == user_id).delete()
#        db.commit()
#        return {"status": "success"}
#    finally:
#       db.close()

# @app.delete("/transactions/{user_id}")
# def delete_transactions(user_id: int):
#    db = SessionLocal()
#    try:
#        db.query(Transaction).filter(Transaction.user_id == user_id).delete()
#        db.commit()
#       return {"status": "success"}
#    finally:
#        db.close()

# @app.delete("/categories/{user_id}")
# def delete_categories(user_id: int):
#    db = SessionLocal()
#    try:
#        db.query(Category).filter(Category.user_id == user_id).delete()
#        db.commit()
#        return {"status": "success"}
#    finally:
#        db.close()
# Part of clear function, put on backlog for future reference

# For testing, run this bash code
# uvicorn frontend.serverAPI:app --reload
# If that gives errors, try:  python -m uvicorn frontend.serverAPI:app --reload
# then go to http://127.0.0.1:8000/goals/1 in your browser to verify that goals for user with ID 1 are visible. Adjust to view different users.
