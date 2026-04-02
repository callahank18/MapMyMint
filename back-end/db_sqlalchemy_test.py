

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
#may need to do:
#pip install SQLAlchemy
#I am using VSCode , so I also had to do 
#ctrl+shift+P, search "Python: select interpreter" and make sure it matched the path where SQLAlchemy was installed

Base = declarative_base()

class User(Base):
    __tablename__ = "Users"  # must match your SQL table name

    CustomerID = Column(Integer, primary_key=True, autoincrement=True)
    Username = Column(String, nullable=False, unique=True)
    Password = Column(String, nullable=False)



#creating the engine creates the connection to the database
engine = create_engine("sqlite:///mapmymint.db", echo=True)


#then, bind the engine to a new session
SessionLocal = sessionmaker(bind=engine)

selectSession = SessionLocal()

#print user table:

all_users = selectSession.query(User).all()

# 5. Print each user
for user in all_users:
    print(f"ID: {user.CustomerID}, Username: {user.Username}, Password: {user.Password}")

# 6. Close the session when done
selectSession.close()



#new_user = User(Username="Vincent", Password="123")
#whenever making a change to the database, you need to stage it:
#session.add(new_user)
#and commit:
#session.commit()




