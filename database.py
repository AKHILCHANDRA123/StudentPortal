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
('23BCE001','student123','Akhil','akhil@gmail.com','9876543210','CSE','2','4')
""")

cursor.execute("""
INSERT OR IGNORE INTO students
(admission_no,password,name,email,phone,department,year,semester)
VALUES
('23BCE002','student123','Janet','janet@gmail.com','9876543211','CSE','2','4')
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

cursor.execute("DELETE FROM attendance")

cursor.executemany("""
INSERT INTO attendance(admission_no,subject,attendance_percent)
VALUES(?,?,?)
""", [

('23BCE001','Python Programming',95),
('23BCE001','Database Management System',91),
('23BCE001','Cloud Computing',92),
('23BCE001','Data Structures',89),
('23BCE001','Operating Systems',94),

('23BCE002','Python Programming',90),
('23BCE002','Database Management System',88),
('23BCE002','Cloud Computing',90),
('23BCE002','Data Structures',92),
('23BCE002','Operating Systems',89)

])



cursor.execute("""
CREATE TABLE IF NOT EXISTS marks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admission_no TEXT,
    subject TEXT,
    marks INTEGER
)
""")

cursor.execute("DELETE FROM marks")

cursor.executemany("""
INSERT INTO marks(admission_no,subject,marks)
VALUES(?,?,?)
""", [

('23BCE001','Python Programming',94),
('23BCE001','Database Management System',90),
('23BCE001','Cloud Computing',85),
('23BCE001','Data Structures',88),
('23BCE001','Operating Systems',92),

('23BCE002','Python Programming',89),
('23BCE002','Database Management System',93),
('23BCE002','Cloud Computing',90),
('23BCE002','Data Structures',91),
('23BCE002','Operating Systems',94)

])



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
VALUES('23BCE001',8.5)
""")

cursor.execute("""
INSERT OR IGNORE INTO results
(admission_no,cgpa)
VALUES('23BCE002',9.1)
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
VALUES('23BCE001',50000,'Paid')
""")

cursor.execute("""
INSERT OR IGNORE INTO fees
(admission_no,amount,status)
VALUES('23BCE002',50000,'Pending')
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
INSERT OR IGNORE INTO statistics(id,total_logins)
VALUES(1,0)
""")

conn.commit()
conn.close()

print("Database Ready!")