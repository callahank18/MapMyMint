import sys
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

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
class GoalCreate(BaseModel):
     user_id: int
     goal_name: str
     target_amount: float
     current_amount: float


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/goals/{user_id}")
def read_goals(user_id: int, db:
    Session = Depends(get_db)):
#the intention here is to use the existing SQLalchemy setup.
#The intent is to query the Goals table for all goals associated with the given user_id and return them as a response.
        goals = db.query(Goals).filter(Goals.user_id == user_id).all()
        return goals

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
# For testing, run this bash code
# uvicorn frontend.fastAPI_test:app --reload
# If that gives errors, try:  python -m uvicorn frontend.fastAPI_test:app --reload
# then go to http://127.0.0.1:8000/goals/1 in your browser to verify that goals for user with ID 1 are visible. Adjust to view different users.