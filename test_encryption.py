from data_service import create_user, login_user, create_goal, get_goals

# Create user
create_user("ryan", "mypassword")

# Login test
print(login_user("ryan", "mypassword"))  # True

# Create goal
create_goal(1, "Buy a bike", 2000)

# Get goals (should be readable text)
print(get_goals(1))
