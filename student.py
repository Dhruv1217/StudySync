from task import task_menu
from attendance import attendance_calculator
from cgpa import calculate_cgpa
from progress import show_progress, weekly_report
from datetime import datetime
from utils import get_random_quote
from file_handler import load_data, save_data
STUDENT_FILE = "data/students.json"

# Student class to store student details
class Student:

    def __init__(self, name, roll_number, branch, semester, email, password):
        self.name = name
        self.roll_number = roll_number
        self.branch = branch
        self.semester = semester
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            "name": self.name,
            "roll_number": self.roll_number,
            "branch": self.branch,
            "semester": self.semester,
            "email": self.email,
            "password": self.password
        }
    
# Function to create a new student account
def create_account():

    students = load_data(STUDENT_FILE)

    print("\n========== Create Account ==========")

    while True:

        name = input("Enter Name : ").strip()

        if name == "":
            print("❌ Name cannot be empty.")

        elif not all(ch.isalpha() or ch.isspace() for ch in name):
            print("❌ Name should contain only letters.")

        else:
            break
    roll_number = input("Enter Roll Number : ")

    # Check duplicate roll number
    for student in students:
        if student["roll_number"] == roll_number:
            print("\n❌ Account already exists with this Roll Number.")
            return

    # Branch Validation
    branches = ["CSE", "CSE AI", "IT", "ECE", "EE", "ME", "CE"]

    while True:
        branch = input("Enter Branch : ").upper().strip()

        if branch in branches:
            break
        else:
            print("❌ Invalid Branch.")

    # Semester Validation
    while True:
        semester = input("Enter Semester (1-8) : ").strip()

        if semester.isdigit():
            semester = int(semester)

            if 1 <= semester <= 8:
                break

        print("❌ Semester must be between 1 and 8.")
    # Email Validation
    while True:

        email = input("Enter Email : ")

        if "@" in email and "." in email:
            break

        print("❌ Invalid Email Address.")


    # Password Validation
    while True:

        password = input("Create Password : ")

        if len(password) < 6:
            print("❌ Password must be at least 6 characters.")
        elif password.isalpha():
            print("❌ Password should contain at least one number.")
        else:
            break

    new_student = Student(
        name,
        roll_number,
        branch,
        semester,
        email,
        password
    )

    students.append(new_student.to_dict())

    save_data(STUDENT_FILE, students)

    print("\n✅ Account Created Successfully!")

# Function to login
def login():

    students = load_data(STUDENT_FILE)

    print("\n========== Login ==========")

    roll_number = input("Enter Roll Number : ")
    password = input("Enter Password : ")

    for student in students:
        if student["roll_number"] == roll_number and student["password"] == password:
            print(f"\n✅ Login Successful!")
            print(f"Welcome {student['name']}")
            return student

    print("\n❌ Invalid Roll Number or Password.")
    return None

# Function to change password
def change_password(student):

    students = load_data(STUDENT_FILE)

    current = input("Enter Current Password : ")

    if current != student["password"]:
        print("❌ Incorrect Password")
        return

    new = input("Enter New Password : ")

    confirm = input("Confirm New Password : ")

    if new != confirm:
        print("❌ Passwords do not match")
        return

    for s in students:

        if s["roll_number"] == student["roll_number"]:

            s["password"] = new
            student["password"] = new

            break

    save_data(STUDENT_FILE, students)

    print("\n✅ Password Changed Successfully!")

def student_dashboard(student):

    while True:

        today = datetime.now()

        date = today.strftime("%d-%m-%Y")
        time = today.strftime("%I:%M %p")

        print("\n" + "=" * 60)
        print("                    STUDYSYNC")
        print("=" * 60)

        print(f"\nWelcome, {student['name']} 👋")

        print(f"\nToday's Date : {date}")
        print(f"Current Time : {time}")

        print("\nQuote of the Day:")
        print(get_random_quote())

        print("\n" + "=" * 60)

        print("1. My Profile")
        print("2. Task Manager")
        print("3. Attendance Calculator")
        print("4. CGPA Calculator")
        print("5. Study Progress")
        print("6. Change Password")
        print("7. Weekly Report")
        print("8. Logout")

        choice = input("\nEnter Choice : ")

        if choice == "1":
            print("\n" + "=" * 50)
            print("           MY PROFILE")
            print("=" * 50)

            print(f"Name       : {student['name']}")
            print(f"Roll No    : {student['roll_number']}")
            print(f"Branch     : {student['branch']}")
            print(f"Semester   : {student['semester']}")
            print(f"Email      : {student['email']}")

            print("=" * 50)

        elif choice == "2":
            task_menu(student)

        elif choice == "3":
            attendance_calculator(student)

        elif choice == "4":
            calculate_cgpa(student)
        elif choice == "5":
            show_progress(student)

        elif choice == "6":
            change_password(student)

        elif choice == "7":
            weekly_report(student)

        elif choice == "8":
            print("\n===================================")
            print(" Thank you for using StudySync 😊")
            print(" Have a Productive Day!")
            print("===================================")
            break

        else:
            print("\nInvalid Choice!")