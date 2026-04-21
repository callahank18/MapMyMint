from backend.db_sqlalchemy_test import SessionLocal, Users, Goals
from backend.security import hash_password, verify_password, encrypt_data, decrypt_data
from sqlalchemy.exc import SQLAlchemyError

# CREATE USER
def create_user(username: str, password: str):
    session = SessionLocal()

    hashed_pw = hash_password(password)

    user = Users(
        Username=username,
        Password=hashed_pw
    )

    session.add(user)
    session.commit()
    session.close()


# LOGIN USER
def login_user(username, password):
    db = SessionLocal()
    try:
        user = db.query(Users).filter(Users.Username == username).first()

        if user is None:
            return {"status": "login_error", "reason": "not_found"}
        if not verify_password(password, user.Password):
            return {"status": "login_error", "reason": "bad_password"}
        if user.Username == username and verify_password(password, user.Password):
            return {"status": "success", "uid":user.CustomerID}
    except SQLAlchemyError as e:
        return {"status": "db_error", "reason": "database_error"}

    



# CREATE GOAL (ENCRYPTED)
def create_goal(user_id: int, goal_name: str, target_amount: float):
    session = SessionLocal()

    encrypted_name = encrypt_data(goal_name)

    goal = Goals(
        user_id=user_id,
        goal_name=encrypted_name,
        target_amount=target_amount
    )

    session.add(goal)
    session.commit()
    session.close()


# GET GOALS (DECRYPTED)
def get_goals(user_id: int):
    session = SessionLocal()

    goals = session.query(Goals).filter(Goals.user_id == user_id).all()

    result = []
    for g in goals:
        result.append({
            "goal_id": g.goal_id,
            "goal_name": decrypt_data(g.goal_name),
            "target_amount": g.target_amount,
            "current_amount": g.current_amount
        })

    session.close()
    return result
