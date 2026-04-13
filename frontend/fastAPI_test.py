import sys
from pathlib import Path
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session


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
        from backend.data_service import get_goals

@app.get("/goals/{user_id}")
def read_goals(user_id: int):
    return get_goals(user_id)


# For testing, run this bash code
# uvicorn fastAPI_test:app --reload
# If that gives errors, try:  python -m uvicorn frontend.fastAPI_test:app --reload
# then go to http://127.0.0.1:8000/goals/1 in your browser to verify that goals for user with ID 1 are visible. Adjust to view different users.
