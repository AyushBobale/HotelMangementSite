import sqlite3
con = sqlite3.connect('Project/static/database/main.db')
sql1 = "SELECT * FROM USERID"
cursor = con.cursor()
cursor.execute(sql1)
rows = cursor.fetchall()
for _ in rows:
  print(_)

sql1 = "SELECT * FROM ERRORLOGGER"
cursor = con.cursor()
cursor.execute(sql1)
rows = cursor.fetchall()
for _ in rows:
  print(_)

