import sqlite3

conn = sqlite3.connect("student.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
id INTEGER PRIMARY KEY AUTOINCREMENT,
admission_no TEXT UNIQUE,
password TEXT,
name TEXT,
email TEXT,
phone TEXT,
department TEXT,
year TEXT,
semester TEXT
)
""")

cursor.execute("""
INSERT OR IGNORE INTO students
(admission_no,password,name,email,phone,department,year,semester)
VALUES
(
'23BCE001',
'student123',
'Akhil',
'akhil@gmail.com',
'9876543210',
'CSE',
'2',
'4'
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admission_no TEXT,
    faculty TEXT,
    subject TEXT,
    rating INTEGER,
    comments TEXT
)
""")

conn.commit()
conn.close()

print("Database Ready!")