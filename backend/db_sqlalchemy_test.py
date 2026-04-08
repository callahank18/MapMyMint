

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, LargeBinary
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import pandas as pd
#may need to do:
#pip install SQLAlchemy
#I am using VSCode , so I also had to do 
#ctrl+shift+P, search "Python: select interpreter" and make sure it matched the path where SQLAlchemy was installed

Base = declarative_base()

class Users(Base):
    __tablename__ = "Users"  # must match your SQL table name

    CustomerID = Column(Integer, primary_key=True, autoincrement=True)
    Username = Column(String, nullable=False, unique=True)
    Password = Column(LargeBinary, nullable=False)
    # optional: relationship to Goals
    goals = relationship("Goals", back_populates="user")


class Goals(Base):
    __tablename__ = "Goals"
    
    goal_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.CustomerID"), nullable=False)
    goal_name = Column(LargeBinary, nullable=False)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0)
    target_date = Column(String, nullable=True)  # or Date if you want proper date handling

    # relationship to User
    user = relationship("Users", back_populates="goals")


class Category(Base):
    __tablename__ = "Categories"

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.CustomerID"), nullable=False)
    name = Column(String, nullable=False)
    parent_category_id = Column(Integer, ForeignKey("Categories.category_id"))
    limit_amount = Column(Float)
     
     # relationships
    user = relationship("User", back_populates="categories")
    parent = relationship("Category", remote_side=[category_id], backref="subcategories")




class Transaction(Base):
    __tablename__ = "Transactions"

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.CustomerID"), nullable=False)
    category_id = Column(Integer, ForeignKey("Categories.category_id"))
    transaction_date = Column(String, nullable=False)
    description = Column(LargeBinary, nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)
    
    user = relationship("User", back_populates="transactions")
    category = relationship("Category")



#creating the engine creates the connection to the database
engine = create_engine("sqlite:///mapmymint.db", echo=True)


#then, bind the engine to a new session
SessionLocal = sessionmaker(bind=engine)

selectSession = SessionLocal()

#query database for all users
all_users = selectSession.query(Users).all()

#iterate through 
for user in all_users:
    print(f"ID: {user.CustomerID}, Username: {user.Username}, Password: {user.Password}")

#close the session when done
selectSession.close()


GoalsSession = SessionLocal()

goals = GoalsSession.query(Goals).filter(Goals.user_id == 1).all()


#Convert to pandas DataFrame
df_goals = pd.DataFrame([{
    "goal_id": g.goal_id,
    "user_id": g.user_id,
    "goal_name": g.goal_name,
    "target_amount": g.target_amount,
    "current_amount": g.current_amount,
    "target_date": g.target_date
} for g in goals])

print(df_goals)

#new_user = User(Username="Vincent", Password="123")
#whenever making a change to the database, you need to stage it:
#session.add(new_user)
#and commit:
#session.commit()




