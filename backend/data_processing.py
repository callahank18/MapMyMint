import pandas as pd
from sqlalchemy.orm import sessionmaker
from db_sqlalchemy_test import Users, Goals, engine
import sqlite3

conn = sqlite3.connect("mapmymint.db")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
conn.close()

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

def get_all_users():
    with SessionLocal() as session:
        users = session.query(Users).all()
        df_users = pd.DataFrame([{
            "CustomerID": u.CustomerID,
            "Username": u.Username,
            "Password": u.Password
        } for u in users])
    return df_users

def get_goals_for_user(user_id):
    with SessionLocal() as session:
        goals = session.query(Goals).filter(Goals.user_id == user_id).all()
        df_goals = pd.DataFrame([{
            "goal_id": g.goal_id,
            "user_id": g.user_id,
            "goal_name": g.goal_name,
            "target_amount": g.target_amount,
            "current_amount": g.current_amount,
            "target_date": g.target_date
        } for g in goals])
    return df_goals

def add_user(username, password):
    with SessionLocal() as session:
        new_user = Users(Username=username, Password=password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user.CustomerID

def add_goal(user_id, goal_name, target_amount, current_amount=0, target_date=None):
    with SessionLocal() as session:
        new_goal = Goals(
            user_id=user_id,
            goal_name=goal_name,
            target_amount=target_amount,
            current_amount=current_amount,
            target_date=target_date
        )
        session.add(new_goal)
        session.commit()
        session.refresh(new_goal)
        return new_goal.goal_id

def update_goal_amount(goal_id, new_amount):
    with SessionLocal() as session:
        goal = session.query(Goals).filter(Goals.goal_id == goal_id).first()
        if goal:
            goal.current_amount = new_amount
            session.commit()
            return True
        return False

def delete_user(user_id):
    with SessionLocal() as session:
        user = session.query(Users).filter(Users.CustomerID == user_id).first()
        if user:
            session.delete(user)
            session.commit()
            return True
        return False

def load_transactions():
    df = pd.read_sql("SELECT * FROM Transactions", engine)
    return df

def clean_transactions(df):
    df = df.drop_duplicates().dropna().copy()
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    return df

def filter_expenses(df):
    return df[df["transaction_type"] == "expense"].copy()

def add_month_column(df):
    df = df.copy()
    df["month"] = df["transaction_date"].dt.to_period("M")
    return df

def categorize_spending(df):
    df = df.copy()
    df["spending_level"] = df["amount"].apply(lambda x: "High" if x > 100 else "Low")
    return df

def sort_by_amount(df):
    return df.sort_values(by="amount", ascending=False)

def total_spent(df):
    return df["amount"].sum()

def spending_by_category(df):
    return df.groupby("category")["amount"].sum()

def monthly_spending(df):
    return df.groupby("month")["amount"].sum()

def process_data():
    df = load_transactions()
    df = clean_transactions(df)
    expenses = filter_expenses(df)
    expenses = add_month_column(expenses)
    expenses = categorize_spending(expenses)
    expenses = sort_by_amount(expenses)

    summary = {
        "total_spent": total_spent(expenses),
        "by_category": spending_by_category(expenses),
        "monthly": monthly_spending(expenses)
    }
    return expenses, summary
