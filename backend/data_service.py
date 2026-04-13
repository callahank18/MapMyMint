from db_sqlalchemy_test import SessionLocal, Users, Goals
from security import hash_password, verify_password, encrypt_data, decrypt_data

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
def login_user(username: str, password: str):
    session = SessionLocal()

    user = session.query(Users).filter(Users.Username == username).first()

    if user and verify_password(password, user.Password):
        session.close()
        return True
    else:
        session.close()
        return False


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
