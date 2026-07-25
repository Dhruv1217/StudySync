from app import app
from models import db, Student, Task, Attendance, CGPA
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_data(filename):
    filepath = os.path.join(BASE_DIR, "data", filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def seed_database():
    with app.app_context():
        # Ensure tables exist
        db.create_all()

        print("Seeding Students...")
        students = load_data("students.json")
        for s in students:
            if not db.session.get(Student, s['roll_number']):
                new_student = Student(
                    name=s.get('name'),
                    roll_number=s.get('roll_number'),
                    branch=s.get('branch'),
                    semester=s.get('semester'),
                    email=s.get('email'),
                    password=s.get('password')
                )
                db.session.add(new_student)
        db.session.commit()

        print("Seeding Tasks...")
        tasks = load_data("tasks.json")
        for t in tasks:
            # Check if task already exists (using a simplistic check)
            if not Task.query.filter_by(id=t.get('task_id')).first():
                new_task = Task(
                    id=t.get('task_id'),
                    roll_number=t.get('roll_number'),
                    title=t.get('title'),
                    subject=t.get('subject'),
                    priority=t.get('priority'),
                    due_date=t.get('due_date'),
                    status=t.get('status')
                )
                db.session.add(new_task)
        db.session.commit()

        print("Seeding Attendance...")
        attendance = load_data("attendance.json")
        for a in attendance:
            if not Attendance.query.filter_by(roll_number=a.get('roll_number')).first():
                new_att = Attendance(
                    roll_number=a.get('roll_number'),
                    total_classes=a.get('total_classes'),
                    attended_classes=a.get('attended_classes'),
                    attendance_percentage=a.get('attendance_percentage')
                )
                db.session.add(new_att)
        db.session.commit()

        print("Seeding CGPA...")
        cgpa = load_data("cgpa.json")
        for c in cgpa:
            if not CGPA.query.filter_by(roll_number=c.get('roll_number')).first():
                new_cgpa = CGPA(
                    roll_number=c.get('roll_number'),
                    semester_sgpa=json.dumps(c.get('semester_sgpa', [])),
                    cgpa=c.get('cgpa')
                )
                db.session.add(new_cgpa)
        db.session.commit()

        print("✅ Database migration complete! You can now safely delete the 'data' folder and 'file_handler.py'.")

if __name__ == "__main__":
    seed_database()
