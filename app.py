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
        session['admission_no'] = student[1]  
        session['name'] = student[3]          
        return redirect(url_for('dashboard')) 

    return render_template('login.html', error="Invalid Admission Number or Password")

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

    return render_template('attendance.html')

@app.route('/timetable')
def timetable():

    if 'admission_no' not in session:
        return redirect(url_for('home'))

    return render_template('timetable.html')

@app.route('/marks')
def marks():

    if 'admission_no' not in session:
        return redirect(url_for('home'))

    return render_template('marks.html')

@app.route('/results')
def results():

    if 'admission_no' not in session:
        return redirect(url_for('home'))

    return render_template('results.html')

@app.route('/fees')
def fees():

    if 'admission_no' not in session:
        return redirect(url_for('home'))

    return render_template('fees.html')


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

    return render_template('admin_dashboard.html')
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
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)