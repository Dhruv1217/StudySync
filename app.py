"""
StudySync – Flask Web Application
==================================
A Student Productivity Management System built with Python & Flask.

Features:
    - Student Authentication (Signup, Login, Logout)
    - Task Management (Add, View, Edit, Delete, Complete)
    - Attendance Calculator
    - CGPA Calculator
    - Study Progress Tracker
    - Weekly Report Generator

Technologies Used:
    - Python (Backend Logic)
    - Flask (Web Framework)
    - Jinja2 (Templating)
    - JSON (Data Storage)
    - HTML/CSS/JS (Frontend)
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils import get_random_quote
from models import db, Student, Task, Attendance, CGPA
import os
import json

# ── Flask App Configuration ──
app = Flask(__name__)
app.secret_key = 'studysync_secret_key_2026'

# ── Database Configuration ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Use DATABASE_URL from environment for Render Postgres, fallback to local sqlite
database_url = os.getenv('DATABASE_URL', f'sqlite:///{os.path.join(BASE_DIR, "studysync.db")}')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Ensure database tables are created before first request
with app.app_context():
    db.create_all()

# ═══════════════════════════════════════════
#  HELPER FUNCTIONS
# ═══════════════════════════════════════════

def get_logged_in_student():
    """Get the currently logged-in student from session."""
    if 'roll_number' not in session:
        return None
    return Student.query.get(session['roll_number'])


def get_student_tasks(roll_number):
    """Get all tasks for a specific student."""
    return Task.query.filter_by(roll_number=roll_number).all()


def get_student_attendance(roll_number):
    """Get attendance record for a student."""
    return Attendance.query.filter_by(roll_number=roll_number).first()


def get_student_cgpa(roll_number):
    """Get CGPA record for a student."""
    return CGPA.query.filter_by(roll_number=roll_number).first()


def calculate_progress_data(roll_number):
    """
    Calculate study progress data for a student.
    Reuses the same logic from progress.py.
    """
    tasks = get_student_tasks(roll_number)

    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks if t.status == 'Completed')
    pending_tasks = total_tasks - completed_tasks

    task_pct = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    attendance_record = get_student_attendance(roll_number)
    attendance_pct = attendance_record.attendance_percentage if attendance_record else 0

    cgpa_record = get_student_cgpa(roll_number)
    cgpa_val = cgpa_record.cgpa if cgpa_record else 0
    cgpa_pct = cgpa_val * 10

    overall = (task_pct + attendance_pct + cgpa_pct) / 3

    if overall >= 90:
        performance = "Excellent ⭐"
    elif overall >= 75:
        performance = "Good 👍"
    elif overall >= 60:
        performance = "Average 🙂"
    else:
        performance = "Needs Improvement 📚"

    return {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'task_pct': task_pct,
        'attendance_pct': attendance_pct,
        'cgpa_val': cgpa_val,
        'cgpa_pct': cgpa_pct,
        'overall': overall,
        'performance': performance
    }


# ═══════════════════════════════════════════
#  LANDING PAGE
# ═══════════════════════════════════════════

@app.route('/')
def index():
    """Landing page with hero section and features."""
    if 'roll_number' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


# ═══════════════════════════════════════════
#  AUTHENTICATION ROUTES
# ═══════════════════════════════════════════

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    """
    Student Registration.
    Validates: name (letters only), roll number (unique), branch, 
    semester (1-8), email, password (min 6 chars + at least 1 number).
    """
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        roll_number = request.form.get('roll_number', '').strip()
        branch = request.form.get('branch', '').strip()
        semester = request.form.get('semester', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        # ── Name Validation ──
        if not name:
            flash('Name cannot be empty.', 'error')
            return redirect(url_for('signup_page'))

        if not all(ch.isalpha() or ch.isspace() for ch in name):
            flash('Name should contain only letters.', 'error')
            return redirect(url_for('signup_page'))

        # ── Duplicate Roll Number Check ──
        existing_student = Student.query.get(roll_number)
        if existing_student:
            flash('Account already exists with this Roll Number.', 'error')
            return redirect(url_for('signup_page'))

        # ── Branch Validation ──
        valid_branches = ['CSE', 'CSE AI', 'IT', 'ECE', 'EE', 'ME', 'CE']
        if branch not in valid_branches:
            flash('Invalid Branch.', 'error')
            return redirect(url_for('signup_page'))

        # ── Semester Validation ──
        if not semester.isdigit() or not (1 <= int(semester) <= 8):
            flash('Semester must be between 1 and 8.', 'error')
            return redirect(url_for('signup_page'))

        # ── Email Validation ──
        if '@' not in email or '.' not in email:
            flash('Invalid Email Address.', 'error')
            return redirect(url_for('signup_page'))

        # ── Password Validation ──
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return redirect(url_for('signup_page'))

        if password.isalpha():
            flash('Password should contain at least one number.', 'error')
            return redirect(url_for('signup_page'))

        # ── Create Student ──
        new_student = Student(
            name=name,
            roll_number=roll_number,
            branch=branch,
            semester=int(semester),
            email=email,
            password=password
        )

        db.session.add(new_student)
        db.session.commit()

        flash('Account Created Successfully! Please login.', 'success')
        return redirect(url_for('login_page'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """
    Student Login.
    Validates roll number and password against stored data.
    """
    if request.method == 'POST':
        roll_number = request.form.get('roll_number', '').strip()
        password = request.form.get('password', '')

        student = Student.query.get(roll_number)
        if student and student.password == password:
            session['roll_number'] = roll_number
            flash(f'Welcome back, {student.name}!', 'success')
            return redirect(url_for('dashboard'))

        flash('Invalid Roll Number or Password.', 'error')
        return redirect(url_for('login_page'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    """Clear session and redirect to landing page."""
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))


# ═══════════════════════════════════════════
#  DASHBOARD
# ═══════════════════════════════════════════

@app.route('/dashboard')
def dashboard():
    """
    Main dashboard with stats overview and quote of the day.
    Uses get_random_quote() from utils.py.
    """
    student = get_logged_in_student()
    if not student:
        flash('Please login first.', 'warning')
        return redirect(url_for('login_page'))

    progress = calculate_progress_data(student.roll_number)
    quote = get_random_quote()

    return render_template('dashboard.html',
                           student=student,
                           quote=quote,
                           total_tasks=progress['total_tasks'],
                           completed_tasks=progress['completed_tasks'],
                           attendance_pct=progress['attendance_pct'],
                           cgpa_val=progress['cgpa_val'])


# ═══════════════════════════════════════════
#  PROFILE
# ═══════════════════════════════════════════

@app.route('/profile')
def profile():
    """Display student profile information."""
    student = get_logged_in_student()
    if not student:
        return redirect(url_for('login_page'))

    return render_template('profile.html', student=student)


# ═══════════════════════════════════════════
#  TASK MANAGEMENT
# ═══════════════════════════════════════════

@app.route('/tasks')
def tasks():
    """View all tasks for the logged-in student."""
    student = get_logged_in_student()
    if not student:
        return redirect(url_for('login_page'))

    student_tasks = get_student_tasks(student.roll_number)
    return render_template('tasks.html', student=student, tasks=student_tasks)


@app.route('/tasks/add', methods=['POST'])
def add_task():
    """Add a new task (mirrors task.py add_task function)."""
    student = get_logged_in_student()
    if not student:
        return redirect(url_for('login_page'))

    new_task = Task(
        roll_number=student.roll_number,
        title=request.form.get('title', '').strip(),
        subject=request.form.get('subject', '').strip(),
        priority=request.form.get('priority', 'Medium'),
        due_date=request.form.get('due_date', '').strip(),
        status='Pending'
    )

    db.session.add(new_task)
    db.session.commit()

    flash('Task Added Successfully!', 'success')
    return redirect(url_for('tasks'))


@app.route('/tasks/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    """Mark a task as completed (mirrors task.py mark_task_completed)."""
    student = get_logged_in_student()
    if not student:
        return redirect(url_for('login_page'))

    task = Task.query.filter_by(id=task_id, roll_number=student.roll_number).first()
    if task:
        task.status = 'Completed'
        db.session.commit()
        flash('Task Marked as Completed!', 'success')
    else:
        flash('Task Not Found!', 'error')

    return redirect(url_for('tasks'))


@app.route('/tasks/edit', methods=['POST'])
def edit_task():
    """Edit an existing task (mirrors task.py edit_task)."""
    student = get_logged_in_student()
    if not student:
        return redirect(url_for('login_page'))

    task_id = int(request.form.get('task_id', 0))
    task = Task.query.filter_by(id=task_id, roll_number=student.roll_number).first()
    
    if task:
        title = request.form.get('title', '').strip()
        subject = request.form.get('subject', '').strip()
        priority = request.form.get('priority', '').strip()
        due_date = request.form.get('due_date', '').strip()

        if title:
            task.title = title
        if subject:
            task.subject = subject
        if priority:
            task.priority = priority
        if due_date:
            task.due_date = due_date

        db.session.commit()
        flash('Task Updated Successfully!', 'success')
    else:
        flash('Task Not Found!', 'error')

    return redirect(url_for('tasks'))


@app.route('/tasks/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    """Delete a task (mirrors task.py delete_task)."""
    student = get_logged_in_student()
    if not student:
        return redirect(url_for('login_page'))

    task = Task.query.filter_by(id=task_id, roll_number=student.roll_number).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        flash('Task Deleted Successfully!', 'success')
    else:
        flash('Task Not Found!', 'error')

    return redirect(url_for('tasks'))


# ═══════════════════════════════════════════
#  ATTENDANCE CALCULATOR
# ═══════════════════════════════════════════

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    """
    Attendance Calculator.
    Mirrors the logic from attendance.py - calculates percentage
    and determines eligibility (>=75%).
    """
    student = get_logged_in_student()
    if not student:
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        try:
            total_classes = int(request.form.get('total_classes', 0))
            attended_classes = int(request.form.get('attended_classes', 0))

            if total_classes <= 0:
                flash('Total classes must be greater than 0.', 'error')
                return redirect(url_for('attendance'))

            if attended_classes < 0 or attended_classes > total_classes:
                flash('Invalid attended classes.', 'error')
                return redirect(url_for('attendance'))

            percentage = (attended_classes / total_classes) * 100

            attendance_record = Attendance.query.filter_by(roll_number=student.roll_number).first()
            if not attendance_record:
                attendance_record = Attendance(roll_number=student.roll_number)
                db.session.add(attendance_record)

            attendance_record.total_classes = total_classes
            attendance_record.attended_classes = attended_classes
            attendance_record.attendance_percentage = round(percentage, 2)
            db.session.commit()

            if percentage >= 75:
                flash(f'Attendance: {percentage:.2f}% — Eligible ✅', 'success')
            else:
                flash(f'Attendance: {percentage:.2f}% — Short Attendance ❌', 'warning')

        except ValueError:
            flash('Please enter valid numbers.', 'error')

        return redirect(url_for('attendance'))

    record = get_student_attendance(student.roll_number)
    return render_template('attendance.html', student=student, record=record)


# ═══════════════════════════════════════════
#  CGPA CALCULATOR
# ═══════════════════════════════════════════

@app.route('/cgpa', methods=['GET', 'POST'])
def cgpa():
    """
    CGPA Calculator.
    Mirrors the logic from cgpa.py - takes semester SGPAs
    and calculates cumulative GPA.
    """
    student = get_logged_in_student()
    if not student:
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        try:
            total_semesters = int(request.form.get('total_semesters', 0))

            if total_semesters < 1 or total_semesters > 8:
                flash('Number of semesters must be between 1 and 8.', 'error')
                return redirect(url_for('cgpa'))

            total_sgpa = 0
            semester_list = []

            for i in range(1, total_semesters + 1):
                sgpa = float(request.form.get(f'sgpa_{i}', 0))

                if sgpa < 0 or sgpa > 10:
                    flash(f'SGPA for Semester {i} should be between 0 and 10.', 'error')
                    return redirect(url_for('cgpa'))

                semester_list.append(sgpa)
                total_sgpa += sgpa

            cgpa_value = total_sgpa / total_semesters

            cgpa_record = CGPA.query.filter_by(roll_number=student.roll_number).first()
            if not cgpa_record:
                cgpa_record = CGPA(roll_number=student.roll_number)
                db.session.add(cgpa_record)

            import json
            cgpa_record.semester_sgpa = json.dumps(semester_list)
            cgpa_record.cgpa = round(cgpa_value, 2)
            db.session.commit()

            flash(f'CGPA Calculated: {cgpa_value:.2f}', 'success')

        except ValueError:
            flash('Please enter valid numbers.', 'error')

        return redirect(url_for('cgpa'))

    cgpa_record = get_student_cgpa(student.roll_number)
    return render_template('cgpa.html', student=student, cgpa_record=cgpa_record)


# ═══════════════════════════════════════════
#  STUDY PROGRESS
# ═══════════════════════════════════════════

@app.route('/progress')
def progress():
    """
    Study Progress.
    Mirrors the logic from progress.py show_progress function.
    Calculates task completion, attendance, CGPA percentages,
    overall score, and performance rating.
    """
    student = get_logged_in_student()
    if not student:
        return redirect(url_for('login_page'))

    data = calculate_progress_data(student.roll_number)

    return render_template('progress.html',
                           student=student,
                           **data)


# ═══════════════════════════════════════════
#  WEEKLY REPORT
# ═══════════════════════════════════════════

@app.route('/report')
def report():
    """
    Weekly Report.
    Mirrors the logic from progress.py weekly_report function.
    """
    student = get_logged_in_student()
    if not student:
        return redirect(url_for('login_page'))

    data = calculate_progress_data(student.roll_number)

    return render_template('report.html',
                           student=student,
                           completed_tasks=data['completed_tasks'],
                           pending_tasks=data['pending_tasks'],
                           attendance_pct=data['attendance_pct'],
                           cgpa_val=data['cgpa_val'])


# ═══════════════════════════════════════════
#  CHANGE PASSWORD
# ═══════════════════════════════════════════

@app.route('/change-password', methods=['GET', 'POST'])
def change_password_page():
    """
    Change Password.
    Mirrors the logic from student.py change_password function.
    """
    student = get_logged_in_student()
    if not student:
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        current = request.form.get('current_password', '')
        new = request.form.get('new_password', '')
        confirm = request.form.get('confirm_password', '')

        if current != student.password:
            flash('Incorrect Current Password.', 'error')
            return redirect(url_for('change_password_page'))

        if new != confirm:
            flash('New passwords do not match.', 'error')
            return redirect(url_for('change_password_page'))

        if len(new) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return redirect(url_for('change_password_page'))

        if new.isalpha():
            flash('Password should contain at least one number.', 'error')
            return redirect(url_for('change_password_page'))

        student.password = new
        db.session.commit()

        flash('Password Changed Successfully!', 'success')
        return redirect(url_for('change_password_page'))

    return render_template('change_password.html', student=student)


# ═══════════════════════════════════════════
#  DELETE ACCOUNT
# ═══════════════════════════════════════════

@app.route('/delete-account', methods=['POST'])
def delete_account():
    """
    Delete Account.
    Deletes the logged in student and all their associated data from the database.
    """
    student = get_logged_in_student()
    if not student:
        return redirect(url_for('login_page'))

    # Delete the student from the database. 
    # Because of cascade="all, delete-orphan" in models.py, this deletes their tasks, attendance, and CGPA too.
    db.session.delete(student)
    db.session.commit()
    
    session.clear()
    flash('Account and all associated data permanently deleted.', 'info')
    return redirect(url_for('index'))


# ═══════════════════════════════════════════
#  RUN APPLICATION
# ═══════════════════════════════════════════

if __name__ == '__main__':

    print("\n" + "=" * 50)
    print("  ⚡ StudySync Web Application")
    print("  🌐 Running at: http://localhost:5000")
    print("=" * 50 + "\n")

    app.run(debug=True, port=5000)
