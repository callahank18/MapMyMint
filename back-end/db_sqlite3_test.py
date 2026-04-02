import sqlite3
import pandas
#in vscode, may need to do: pip install pandas

conn = sqlite3.connect("MapMyMint.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM Users")
rows = cursor.fetchall()

for row in rows:
    print(row)


'''
cursor.execute(
    "INSERT INTO Users (Username, Password) VALUES (?, ?)",
    ("Bob", "pass123")
)
'''

# Commit the change
conn.commit()



conn.close()