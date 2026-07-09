from datetime import datetime

start_time = datetime.now()
active_users = 0

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():

    admission_no = request.form['admission_no']
    password = request.form['password']

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE admission_no=? AND password=?",
        (admission_no, password)
    )

    student = cursor.fetchone()
    conn.close()

    if student:

        global active_users

        active_users += 1

        session['admission_no'] = student[1]
        session['name'] = student[3]

        conn = sqlite3.connect('student.db')
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE statistics SET total_logins = total_logins + 1 WHERE id = 1"
        )

        cursor.execute(
            """
            INSERT INTO logs(admission_no, action, time)
            VALUES (?, ?, ?)
            """,
            (
                student[1],
                "Logged In",
                datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            )
        )

        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))

    return render_template(
        'login.html',
        error="Invalid Admission Number or Password"
    )

@app.route('/dashboard')
def dashboard():

    if 'admission_no' not in session:
        return redirect(url_for('home'))

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE admission_no=?",
        (session['admission_no'],)
    )

    student = cursor.fetchone()

    conn.close()

    return render_template('dashboard.html', student=student)

@app.route('/profile')
def profile():

    if 'admission_no' not in session:
        return redirect(url_for('home'))

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE admission_no=?",
        (session['admission_no'],)
    )

    student = cursor.fetchone()

    conn.close()

    return render_template('profile.html', student=student)

@app.route('/attendance')
def attendance():

    if 'admission_no' not in session:
        return redirect(url_for('home'))

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT subject, attendance_percent FROM attendance WHERE admission_no=?",
        (session['admission_no'],)
    )

    attendance = cursor.fetchall()

    conn.close()

    return render_template(
        'attendance.html',
        attendance=attendance
    )

@app.route('/timetable')
def timetable():

    if 'admission_no' not in session:
        return redirect(url_for('home'))

    return render_template('timetable.html')

@app.route('/marks')
def marks():

    if 'admission_no' not in session:
        return redirect(url_for('home'))

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT subject, marks FROM marks WHERE admission_no=?",
        (session['admission_no'],)
    )

    marks = cursor.fetchall()

    conn.close()

    return render_template('marks.html', marks=marks)

@app.route('/results')
def results():

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT cgpa FROM results WHERE admission_no=?",
        (session['admission_no'],)
    )

    result = cursor.fetchone()

    conn.close()

    return render_template('results.html', result=result)

@app.route('/fees')
def fees():

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT amount,status FROM fees WHERE admission_no=?",
        (session['admission_no'],)
    )

    fee = cursor.fetchone()

    conn.close()

    return render_template('fees.html', fee=fee)


@app.route('/feedback')
def feedback():

    if 'admission_no' not in session:
        return redirect(url_for('home'))

    return render_template('feedback.html')
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():

    faculty = request.form['faculty']
    subject = request.form['subject']
    rating = request.form['rating']
    comments = request.form['comments']

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO feedback
        (admission_no, faculty, subject, rating, comments)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            session['admission_no'],
            faculty,
            subject,
            rating,
            comments
        )
    )

    conn.commit()
    conn.close()

    return """
    <h2>Feedback Submitted Successfully!</h2>
    <a href='/dashboard'>Back to Dashboard</a>
    """
@app.route('/admin')
def admin():
    return render_template('admin.html')
@app.route('/admin_login', methods=['POST'])
def admin_login():

    username = request.form['username']
    password = request.form['password']

    if username == "admin" and password == "admin123":
        session['admin'] = True
        return redirect(url_for('admin_dashboard'))

    return "Invalid Admin Login"
@app.route('/admin_dashboard')
def admin_dashboard():

    if 'admin' not in session:
        return redirect(url_for('admin'))

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM feedback")
    total_feedback = cursor.fetchone()[0]

    conn.close()

    return render_template(
        'admin_dashboard.html',
        total_students=total_students,
        total_feedback=total_feedback
    )
@app.route('/monitor')
def monitor():

    if 'admin' not in session:
        return redirect(url_for('admin'))

    uptime = datetime.now() - start_time

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute("SELECT total_logins FROM statistics WHERE id=1")
    total_logins = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM feedback")
    total_feedback = cursor.fetchone()[0]

    cursor.execute("""
        SELECT admission_no, action, time
        FROM logs
        ORDER BY id DESC
        LIMIT 10
    """)
    logs = cursor.fetchall()

    conn.close()

    return render_template(
        'monitor.html',
        active_users=active_users,
        uptime=uptime,
        total_logins=total_logins,
        total_students=total_students,
        total_feedback=total_feedback,
        logs=logs
    )


@app.route('/admin_logout')
def admin_logout():

    session.pop('admin', None)

    return redirect(url_for('admin'))

@app.route('/view_feedback')
def view_feedback():

    if 'admin' not in session:
        return redirect(url_for('admin'))

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM feedback")

    feedbacks = cursor.fetchall()

    conn.close()

    return render_template(
        'view_feedback.html',
        feedbacks=feedbacks
    )
@app.route('/logout')
def logout():

    global active_users

    if active_users > 0:
        active_users -= 1

    if 'admission_no' in session:

        conn = sqlite3.connect('student.db')
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO logs(admission_no, action, time)
            VALUES (?, ?, ?)
            """,
            (
                session['admission_no'],
                "Logged Out",
                datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            )
        )

        conn.commit()
        conn.close()

    session.clear()

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)