from contextlib import closing
from datetime import datetime
import os
import sqlite3

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash


DATABASE = "student.db"
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH")

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

start_time = datetime.now()
active_users = 0


def fetch_one(query, params=()):
    with closing(sqlite3.connect(DATABASE)) as conn:
        return conn.execute(query, params).fetchone()


def fetch_all(query, params=()):
    with closing(sqlite3.connect(DATABASE)) as conn:
        return conn.execute(query, params).fetchall()


def require_student_login():
    if "admission_no" not in session:
        return redirect(url_for("home"))
    return None


def require_admin_login():
    if "admin" not in session:
        return redirect(url_for("admin"))
    return None


def current_admission_no():
    return session["admission_no"]


def get_current_student():
    return fetch_one(
        "SELECT * FROM students WHERE admission_no=?",
        (current_admission_no(),),
    )


def record_student_log(admission_no, action):
    with closing(sqlite3.connect(DATABASE)) as conn:
        conn.execute(
            """
            INSERT INTO logs(admission_no, action, time)
            VALUES (?, ?, ?)
            """,
            (admission_no, action, datetime.now().strftime("%d-%m-%Y %H:%M:%S")),
        )
        conn.commit()


def admin_credentials_configured():
    return bool(ADMIN_USERNAME and ADMIN_PASSWORD_HASH)


def valid_admin_login(username, password):
    if not admin_credentials_configured():
        return False

    return username == ADMIN_USERNAME and check_password_hash(
        ADMIN_PASSWORD_HASH,
        password,
    )


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    admission_no = request.form.get("admission_no", "").strip()
    password = request.form.get("password", "")

    student = fetch_one(
        "SELECT * FROM students WHERE admission_no=? AND password=?",
        (admission_no, password),
    )

    if student:
        global active_users
        active_users += 1

        session["admission_no"] = student[1]
        session["name"] = student[3]

        with closing(sqlite3.connect(DATABASE)) as conn:
            conn.execute(
                "UPDATE statistics SET total_logins = total_logins + 1 WHERE id = 1"
            )
            conn.commit()

        record_student_log(student[1], "Logged In")

        return redirect(url_for("dashboard"))

    return render_template("login.html", error="Invalid Admission Number or Password")


@app.route("/dashboard")
def dashboard():
    auth_redirect = require_student_login()
    if auth_redirect:
        return auth_redirect

    return render_template("dashboard.html", student=get_current_student())


@app.route("/profile")
def profile():
    auth_redirect = require_student_login()
    if auth_redirect:
        return auth_redirect

    return render_template("profile.html", student=get_current_student())


@app.route("/attendance")
def attendance():
    auth_redirect = require_student_login()
    if auth_redirect:
        return auth_redirect

    attendance_rows = fetch_all(
        "SELECT subject, attendance_percent FROM attendance WHERE admission_no=?",
        (current_admission_no(),),
    )

    return render_template("attendance.html", attendance=attendance_rows)


@app.route("/timetable")
def timetable():
    auth_redirect = require_student_login()
    if auth_redirect:
        return auth_redirect

    return render_template("timetable.html")


@app.route("/marks")
def marks():
    auth_redirect = require_student_login()
    if auth_redirect:
        return auth_redirect

    marks_rows = fetch_all(
        "SELECT subject, marks FROM marks WHERE admission_no=?",
        (current_admission_no(),),
    )

    return render_template("marks.html", marks=marks_rows)


@app.route("/results")
def results():
    auth_redirect = require_student_login()
    if auth_redirect:
        return auth_redirect

    result = fetch_one(
        "SELECT cgpa FROM results WHERE admission_no=?",
        (current_admission_no(),),
    )

    return render_template("results.html", result=result)


@app.route("/fees")
def fees():
    auth_redirect = require_student_login()
    if auth_redirect:
        return auth_redirect

    fee = fetch_one(
        "SELECT amount, status FROM fees WHERE admission_no=?",
        (current_admission_no(),),
    )

    return render_template("fees.html", fee=fee)


@app.route("/feedback")
def feedback():
    auth_redirect = require_student_login()
    if auth_redirect:
        return auth_redirect

    return render_template("feedback.html")


@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    auth_redirect = require_student_login()
    if auth_redirect:
        return auth_redirect

    faculty = request.form.get("faculty", "").strip()
    subject = request.form.get("subject", "").strip()
    rating = request.form.get("rating", "").strip()
    comments = request.form.get("comments", "").strip()

    with closing(sqlite3.connect(DATABASE)) as conn:
        conn.execute(
            """
            INSERT INTO feedback
            (admission_no, faculty, subject, rating, comments)
            VALUES (?, ?, ?, ?, ?)
            """,
            (current_admission_no(), faculty, subject, rating, comments),
        )
        conn.commit()

    return """
    <h2>Feedback Submitted Successfully!</h2>
    <a href='/dashboard'>Back to Dashboard</a>
    """


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/admin_login", methods=["POST"])
def admin_login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    if not admin_credentials_configured():
        return (
            "Admin login is not configured. Set ADMIN_USERNAME and "
            "ADMIN_PASSWORD_HASH environment variables.",
            503,
        )

    if valid_admin_login(username, password):
        session["admin"] = True
        return redirect(url_for("admin_dashboard"))

    return "Invalid Admin Login"


@app.route("/admin_dashboard")
def admin_dashboard():
    auth_redirect = require_admin_login()
    if auth_redirect:
        return auth_redirect

    total_students = fetch_one("SELECT COUNT(*) FROM students")[0]
    total_feedback = fetch_one("SELECT COUNT(*) FROM feedback")[0]

    return render_template(
        "admin_dashboard.html",
        total_students=total_students,
        total_feedback=total_feedback,
    )


@app.route("/monitor")
def monitor():
    auth_redirect = require_admin_login()
    if auth_redirect:
        return auth_redirect

    uptime = datetime.now() - start_time
    total_logins = fetch_one("SELECT total_logins FROM statistics WHERE id=1")[0]
    total_students = fetch_one("SELECT COUNT(*) FROM students")[0]
    total_feedback = fetch_one("SELECT COUNT(*) FROM feedback")[0]
    logs = fetch_all(
        """
        SELECT admission_no, action, time
        FROM logs
        ORDER BY id DESC
        LIMIT 10
        """
    )

    return render_template(
        "monitor.html",
        active_users=active_users,
        uptime=uptime,
        total_logins=total_logins,
        total_students=total_students,
        total_feedback=total_feedback,
        logs=logs,
    )


@app.route("/admin_logout")
def admin_logout():
    session.pop("admin", None)

    return redirect(url_for("admin"))


@app.route("/view_feedback")
def view_feedback():
    auth_redirect = require_admin_login()
    if auth_redirect:
        return auth_redirect

    feedbacks = fetch_all("SELECT * FROM feedback")

    return render_template("view_feedback.html", feedbacks=feedbacks)


@app.route("/cloud")
def cloud():
    auth_redirect = require_student_login()
    if auth_redirect:
        return auth_redirect

    return render_template("cloud_deployement.html")


@app.route("/logout")
def logout():
    global active_users

    if active_users > 0:
        active_users -= 1

    if "admission_no" in session:
        record_student_log(current_admission_no(), "Logged Out")

    session.clear()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
