import sqlite3

conn = sqlite3.connect('student.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM students")

for row in cursor.fetchall():
    print(row)

conn.close()