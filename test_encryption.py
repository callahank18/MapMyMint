from backend.data_service import create_user, login_user, create_goal, get_goals
from backend.db_sqlalchemy_test import SessionLocal, Users, Goals

print("\n--- TEST START ---\n")

# 1. Create user
create_user("testuser", "securepass")

# 2. Verify login works
login_result = login_user("testuser", "securepass")
print("Login success:", login_result)

# 3. Create goal (this should be encrypted in DB)
create_goal(1, "Secret Goal", 5000)

# 4. Fetch goals (should be decrypted when returned)
goals = get_goals(1)
print("Decrypted goals from system:", goals)


# =========================
# 🔍 DIRECT DATABASE CHECK
# =========================
print("\n--- RAW DATABASE CHECK ---\n")

session = SessionLocal()

# Check stored password
user = session.query(Users).filter(Users.Username == "testuser").first()
print("Stored password (should NOT be plain text):", user.Password)

# Check stored goal name
goal = session.query(Goals).filter(Goals.user_id == 1).first()
print("Stored goal_name (should be encrypted bytes):", goal.goal_name)

session.close()

print("\n--- TEST END ---\n")
