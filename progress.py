from file_handler import load_data

TASK_FILE = "data/tasks.json"
ATTENDANCE_FILE = "data/attendance.json"
CGPA_FILE = "data/cgpa.json"

# Display student progress
def show_progress(student):

    tasks = load_data(TASK_FILE)
    attendance = load_data(ATTENDANCE_FILE)
    cgpa = load_data(CGPA_FILE)

    total_tasks = 0
    completed_tasks = 0

    for task in tasks:
        if task["roll_number"] == student["roll_number"]:
            total_tasks += 1
            if task["status"] == "Completed":
                completed_tasks += 1

    pending_tasks = total_tasks - completed_tasks

    task_percentage = 0

    if total_tasks > 0:
        task_percentage = (completed_tasks / total_tasks) * 100

    attendance_percentage = 0

    for record in attendance:
        if record["roll_number"] == student["roll_number"]:
            attendance_percentage = record["attendance_percentage"]
            break

    cgpa_value = 0

    for record in cgpa:
        if record["roll_number"] == student["roll_number"]:
            cgpa_value = record["cgpa"]
            break

    cgpa_percentage = cgpa_value * 10

    overall = (task_percentage + attendance_percentage + cgpa_percentage) / 3

    if overall >= 90:
        performance = "Excellent ⭐"

    elif overall >= 75:
        performance = "Good 👍"

    elif overall >= 60:
        performance = "Average 🙂"

    else:
        performance = "Needs Improvement 📚"

    print("\n" + "="*50)
    print("             STUDY PROGRESS")
    print("="*50)

    print("Student Name     :", student["name"])
    print("Completed Tasks  :", completed_tasks)
    print("Pending Tasks    :", pending_tasks)
    print(f"Task Completion  : {task_percentage:.2f}%")
    print(f"Attendance       : {attendance_percentage:.2f}%")
    print(f"CGPA             : {cgpa_value:.2f}")
    print(f"Overall Score    : {overall:.2f}%")
    print("Performance      :", performance)

    print("="*50)

# Display weekly report
def weekly_report(student):

    tasks = load_data(TASK_FILE)
    attendance = load_data(ATTENDANCE_FILE)
    cgpa = load_data(CGPA_FILE)

    total_tasks = 0
    completed_tasks = 0

    for task in tasks:
        if task["roll_number"] == student["roll_number"]:
            total_tasks += 1

            if task["status"] == "Completed":
                completed_tasks += 1

    pending_tasks = total_tasks - completed_tasks

    attendance_percentage = 0

    for record in attendance:
        if record["roll_number"] == student["roll_number"]:
            attendance_percentage = record["attendance_percentage"]
            break

    cgpa_value = 0

    for record in cgpa:
        if record["roll_number"] == student["roll_number"]:
            cgpa_value = record["cgpa"]
            break

    print("\n" + "=" * 55)
    print("                 WEEKLY REPORT")
    print("=" * 55)

    print(f"Student Name      : {student['name']}")
    print(f"Completed Tasks   : {completed_tasks}")
    print(f"Pending Tasks     : {pending_tasks}")
    print(f"Attendance        : {attendance_percentage:.2f}%")
    print(f"CGPA              : {cgpa_value:.2f}")

    print("=" * 55)