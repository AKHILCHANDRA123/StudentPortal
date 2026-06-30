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
INSERT OR IGNORE INTO students
(admission_no,password,name,email,phone,department,year,semester)
VALUES
(
'23BCE002',
'student123',
'Janet',
'Janet@gmail.com',
'9876543211',
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

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(
id INTEGER PRIMARY KEY AUTOINCREMENT,
admission_no TEXT,
subject TEXT,
attendance_percent INTEGER
)
""")

cursor.execute("""
INSERT OR IGNORE INTO attendance
(admission_no,subject,attendance_percent)
VALUES
('23BCE001','Cloud Computing',92)
""")

cursor.execute("""
INSERT OR IGNORE INTO attendance
(admission_no,subject,attendance_percent)
VALUES
('23BCE002','Cloud Computing',88)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS marks(
id INTEGER PRIMARY KEY AUTOINCREMENT,
admission_no TEXT,
subject TEXT,
marks INTEGER
)
""")

cursor.execute("""
INSERT OR IGNORE INTO marks
(admission_no,subject,marks)
VALUES
('23BCE001','Cloud Computing',85)
""")

cursor.execute("""
INSERT OR IGNORE INTO marks
(admission_no,subject,marks)
VALUES
('23BCE002','Cloud Computing',90)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS results(
id INTEGER PRIMARY KEY AUTOINCREMENT,
admission_no TEXT,
cgpa REAL
)
""")

cursor.execute("""
INSERT OR IGNORE INTO results
(admission_no,cgpa)
VALUES
('23BCE001',8.5)
""")

cursor.execute("""
INSERT OR IGNORE INTO results
(admission_no,cgpa)
VALUES
('23BCE002',9.1)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS fees(
id INTEGER PRIMARY KEY AUTOINCREMENT,
admission_no TEXT,
amount INTEGER,
status TEXT
)
""")

cursor.execute("""
INSERT OR IGNORE INTO fees
(admission_no,amount,status)
VALUES
('23BCE001',50000,'Paid')
""")

cursor.execute("""
INSERT OR IGNORE INTO fees
(admission_no,amount,status)
VALUES
('23BCE002',50000,'Pending')
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admission_no TEXT,
    action TEXT,
    time TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS statistics(
    id INTEGER PRIMARY KEY,
    total_logins INTEGER
)
""")

cursor.execute("""
INSERT OR IGNORE INTO statistics
(id,total_logins)
VALUES(1,0)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS statistics(
id INTEGER PRIMARY KEY,
total_logins INTEGER
)
""")

cursor.execute("""
INSERT OR IGNORE INTO statistics
VALUES(1,0)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS logs(
id INTEGER PRIMARY KEY AUTOINCREMENT,
admission_no TEXT,
action TEXT,
time TEXT
)
""")
conn.commit()
conn.close()

print("Database Ready!")