import sqlite3 as sql
import pandas as pd
#in vscode, may need to do: pip install pandas

conn = sql.connect("MapMyMint.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM Users")
rows = cursor.fetchall()

for row in rows:
    print(row)


cursor.execute("SELECT * FROM Goals WHERE user_id=1")
goals = cursor.fetchall()
for goal in goals:
    print(goal)

'''
goals is a list of tuples
goals = [
    (1, 1, "Vacation", 2000.0, 500.0, "2026-12-31"),
    (2, 1, "New Laptop", 1500.0, 300.0, "2026-06-30"),
    ...
]

'''

#it can be turned into a pandas DataFrame 
df_goals = pd.DataFrame(
    goals,
    columns=["goal_id", "user_id", "goal_name", "target_amount", "current_amount", "target_date"]
)

print(df_goals)
'''
cursor.execute(
    "INSERT INTO Users (Username, Password) VALUES (?, ?)",
    ("Bob", "pass123")
)
'''

# Commit the change
conn.commit()



conn.close()