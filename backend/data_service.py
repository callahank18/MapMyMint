from backend.models import SessionLocal, Users, Goals, Transaction, Category
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
    with SessionLocal() as db:
        try:
            # Check for duplicate username before inserting
            existing = db.query(Users).filter(Users.Username == username).first()
            if existing:
                return {"status": "register_error", "reason": "user_exists"}
 
            # Decode bytes to string for DB String column storage
            hashed_pw = hash_password(password).decode('utf-8')
            user = Users(Username=username, Password=hashed_pw)
 
            db.add(user)
            db.commit()
            db.refresh(user)
 
            return {"status": "success", "user_id": user.CustomerID}
 
        except SQLAlchemyError:
            db.rollback()
            return {"status": "db_error", "reason": "database_error"}



def login_user(username: str, password: str):
    with SessionLocal() as db:
        try:
            user = db.query(Users).filter(Users.Username == username).first()
 
            if user is None:
                return {"status": "login_error", "reason": "not_found"}
 
            # Re-encode stored string back to bytes before verifying
            if not verify_password(password, user.Password.encode('utf-8')):
                return {"status": "login_error", "reason": "bad_password"}
 
            return {"status": "success", "user_id": user.CustomerID}
 
        except SQLAlchemyError:
            return {"status": "db_error", "reason": "database_error"}


# ------------------------
# CREATE GOAL (ENCRYPTED)
# ------------------------
def create_goal(user_id: int, goal_name: str, target_amount: float):
    with SessionLocal() as session:
        try:

            # Encrypt goal name
            encrypted_name = encrypt_data(goal_name).decode('utf-8')

            new_goal = Goals(
                user_id=user_id,
                goal_name=encrypted_name,
                target_amount=target_amount,
                current_amount=0
            )

            session.add(new_goal)
            session.commit()
            session.refresh(new_goal) #pulls the new goal

            return {"status": "success", "goal_id": new_goal.goal_id}
        except SQLAlchemyError as e:
            session.rollback()
            return {"status": "db_error", "reason": str(e)}


# ------------------------
# GET GOALS (DECRYPTED)
# ------------------------
def get_goals(user_id: int):
    with SessionLocal() as session:
        try:
            goals = session.query(Goals).filter(Goals.user_id == user_id).all()

            result = []
            for g in goals:
                raw_data = g.goal_name.encode('utf-8') if isinstance(g.goal_name, str) else g.goal_name
                result.append({
                    "goal_id": g.goal_id,
                    "user_id": g.user_id,
                    "goal_name": decrypt_data(raw_data),  # 🔓 decrypted here
                    "target_amount": g.target_amount,
                    "current_amount": g.current_amount,
                    "target_date": g.target_date
                })

            return result
        except SQLAlchemyError as e:
            return {"status": "db_error", "reason": str(e)}
#----------------
# Update goals
#---------------------
def update_goal_amount(goal_id: int, new_amount: float):
    with SessionLocal() as session:
        try:
            goal = session.query(Goals).filter(Goals.goal_id == goal_id).first()
            if goal:
                goal.current_amount = new_amount
                session.commit()
                return {"status": "success"}
            return {"status": "error", "reason": "not_found"}
        except SQLAlchemyError as e:
            session.rollback()
            return {"status": "db_error", "reason": str(e)}

# ------------------------
# CREATE Transaction
# ------------------------
def create_transaction(user_id: int, description: str, amount: float, category_id: int = None, date: str = None, t_type: str = "expense"):
    with SessionLocal() as session:
        try:
            new_tx = Transaction(
                user_id = user_id,
                description = description,
                amount = amount,
                category_id = category_id,
                transaction_date = date or "2026-01-01", #Generic date to fall back to
                transaction_type= t_type
            )
            session.add(new_tx)
            session.commit()
            session.refresh(new_tx)

            return {"status": "success", "transaction_id": new_tx.transaction_id}
        except SQLAlchemyError as e:
            session.rollback()
            return {"status": "db_error", "reason": str(e)}
        
# ------------------------
# GET Transaction
# ------------------------
def get_transactions(user_id: int):
    with SessionLocal() as session:
        try:
            txs = session.query(Transaction).filter(Transaction.user_id == user_id).all()
        
            return [{
                "id": t.transaction_id,
                "description": t.description,
                "amount": t.amount,
                "date": t.transaction_date,
                "category_id": t.category_id,
                "type": t.transaction_type
            } for t in txs]
        except SQLAlchemyError as e:
            return {"status": "db_error", "reason": str(e)}    

# Logic update for fetching transactions
def get_transactions_with_names(user_id: int):
    with SessionLocal() as session:
        try:
            # We join Transaction and Category to pull the 'name' field from Categories
            results = session.query(Transaction, Category.name).outerjoin(Category, Transaction.category_id == Category.category_id).filter(Transaction.user_id == user_id).all()
            return [{
                "id": t.Transaction.transaction_id,
                "description": t.Transaction.description,
                "amount": t.Transaction.amount,
                "date": t.Transaction.transaction_date,
                "category_name": t.name if t.name else "Uncategorized", # This comes from the join
                "type": t.Transaction.transaction_type
            } for t in results]
        except SQLAlchemyError as e:
            return {"status": "db_error", "reason": str(e)}
        
# CREATE CATEGORY
# ------------------------
def create_category(user_id: int, name: str, limit_amount: float = 0, parent_id: int = None):
    with SessionLocal() as session:
        try:
            new_cat = Category(
                user_id=user_id,
                name=name,
                limit_amount=limit_amount,
                parent_category_id=parent_id
            )
            session.add(new_cat)
            session.commit()
            session.refresh(new_cat)
            return {"status": "success", "category_id": new_cat.category_id}
        except SQLAlchemyError as e:
            session.rollback()
            return {"status": "db_error", "reason": str(e)}
        
# get Categories
# ------------------
def get_categories(user_id: int):
    with SessionLocal() as session:
        try:
            cats = session.query(Category).filter(Category.user_id == user_id).all()
            return [{
                "id": c.category_id,
                "name": c.name,
                "limit": c.limit_amount,
                "parent_id": c.parent_category_id
            } for c in cats]
        except SQLAlchemyError as e:
            return {"status": "db_error", "reason": str(e)}
    