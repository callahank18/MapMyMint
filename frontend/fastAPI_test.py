import sys
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.data_service import *

# Add the parent directory to the system path to allow imports from the backend directory
sys.path.append(str(Path(__file__).resolve().parent.parent))


from backend.db_sqlalchemy_test import SessionLocal, Goals #Intending on taking the existing data setup and working with it

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
class GoalCreate(BaseModel):
     user_id: int
     goal_name: str
     target_amount: float
     current_amount: float

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
        return result


@app.post("/register/")
def createUser(user: LoginSchema):
    result = create_user(user.username, user.password)
    return result


@app.get("/goals/{user_id}")
def read_goals(user_id: int):
    #the intention here is to use the existing SQLalchemy setup.
    #The intent is to query the Goals table for all goals associated with the given user_id and return them as a response.
    print("userid:", user_id)
    return get_goals(user_id)

@app.post("/goals/")
def create_goal(goal: GoalCreate, db: Session = Depends(get_db)):
    try:
        # Create the SQLAlchemy model instance from the Pydantic data
        new_goal = Goals(
            user_id=goal.user_id,
            goal_name=goal.goal_name,
            target_amount=goal.target_amount,
            current_amount=goal.current_amount
        )
        db.add(new_goal)
        db.commit()
        db.refresh(new_goal)
        return {"status": "success", "goal_id": new_goal.goal_id}
    except Exception as e:
        db.rollback() # Undo if something goes wrong
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

@app.put("/goals/{goal_id}")
def update_goal(goal_id: int, goal_update: GoalUpdate, db: Session = Depends(get_db)):
    try:
        # Find the goal by ID
        goal = db.query(Goals).filter(Goals.goal_id == goal_id).first()
        if not goal:
            raise HTTPException(status_code=404, detail=f"Goal with ID {goal_id} not found")
        
        # Update the current_amount
        goal.current_amount = goal_update.current_amount
        db.commit()
        db.refresh(goal)
        return {"status": "success", "goal_id": goal.goal_id, "current_amount": goal.current_amount}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
# For testing, run this bash code
# uvicorn frontend.fastAPI_test:app --reload
# If that gives errors, try:  python -m uvicorn frontend.fastAPI_test:app --reload
# then go to http://127.0.0.1:8000/goals/1 in your browser to verify that goals for user with ID 1 are visible. Adjust to view different users.
