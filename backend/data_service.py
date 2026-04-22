from backend.db_sqlalchemy_test import SessionLocal, Users, Goals
from sqlalchemy.exc import SQLAlchemyError
from backend.security import (
    hash_password,
    verify_password,
    encrypt_data,
    decrypt_data
)


# ------------------------
# CREATE USER
# ------------------------
def create_user(username: str, password: str):
    db = SessionLocal()
    try:

        user = db.query(Users).filter(Users.Username == username).first()
        if user:
            return {"status": "register_error", "reason": "user_exists"}

        hashed_pw = hash_password(password)

        user = Users(
            Username=username,
            Password=hashed_pw
        )
        db.add(user)
        db.commit()
        db.close()
        print(f"User '{username}' created successfully")
        return {"status": "success"}
            


    except SQLAlchemyError as e:
        return {"status": "db_error", "reason": "database_error"}







def login_user(username, password):
    db = SessionLocal()
    try:
        user = db.query(Users).filter(Users.Username == username).first()

        if user is None:
            db.close()
            return {"status": "login_error", "reason": "not_found"}
        if not verify_password(password, user.Password):
            db.close()
            return {"status": "login_error", "reason": "bad_password"}
        if user.Username == username and verify_password(password, user.Password):
            db.close()
            return {"status": "success", "user_id":user.CustomerID}
    except SQLAlchemyError as e:
        return {"status": "db_error", "reason": "database_error"}


# ------------------------
# CREATE GOAL (ENCRYPTED)
# ------------------------
def create_goal(user_id: int, goal_name: str, target_amount: float):
    session = SessionLocal()

    # Encrypt goal name
    encrypted_name = encrypt_data(goal_name)

    new_goal = Goals(
        user_id=user_id,
        goal_name=encrypted_name,
        target_amount=target_amount,
        current_amount=0
    )

    session.add(new_goal)
    session.commit()
    session.close()

    print("Goal created successfully")


# ------------------------
# GET GOALS (DECRYPTED)
# ------------------------
def get_goals(user_id: int):
    session = SessionLocal()

    goals = session.query(Goals).filter(Goals.user_id == user_id).all()

    result = []
    for g in goals:
        result.append({
            "goal_id": g.goal_id,
            "user_id": g.user_id,
            "goal_name": decrypt_data(g.goal_name),  # 🔓 decrypted here
            "target_amount": g.target_amount,
            "current_amount": g.current_amount,
            "target_date": g.target_date
        })

    session.close()
    return result
