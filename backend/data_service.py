from backend.db_sqlalchemy_test import SessionLocal, Users, Goals
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
    session = SessionLocal()

    # Check if user already exists
    existing_user = session.query(Users).filter_by(Username=username).first()
    if existing_user:
        print("User already exists")
        session.close()
        return False

    # Hash password
    hashed_pw = hash_password(password)

    # Create new user
    new_user = Users(
        Username=username,
        Password=hashed_pw
    )

    session.add(new_user)
    session.commit()
    session.close()

    print(f"User '{username}' created successfully")
    return True


# ------------------------
# LOGIN USER
# ------------------------
def login_user(username: str, password: str) -> bool:
    session = SessionLocal()

    user = session.query(Users).filter_by(Username=username).first()

    if not user:
        session.close()
        return False

    # Verify hashed password
    is_valid = verify_password(password, user.Password)

    session.close()
    return is_valid


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
