from file_handler import load_data, save_data

TASK_FILE = "data/tasks.json"

# Task class
class Task:

    def __init__(self, task_id, roll_number, title, subject, priority, due_date, status="Pending"):
        self.task_id = task_id
        self.roll_number = roll_number
        self.title = title
        self.subject = subject
        self.priority = priority
        self.due_date = due_date
        self.status = status

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "roll_number": self.roll_number,
            "title": self.title,
            "subject": self.subject,
            "priority": self.priority,
            "due_date": self.due_date,
            "status": self.status
        }
    
# Add a new task
def add_task(student):

    tasks = load_data(TASK_FILE)

    print("\n========== ADD TASK ==========")

    task_id = len(tasks) + 1

    title = input("Enter Task Title : ")
    subject = input("Enter Subject : ")
    priority = input("Enter Priority (High/Medium/Low) : ")
    due_date = input("Enter Due Date (DD-MM-YYYY) : ")

    new_task = Task(
        task_id,
        student["roll_number"],
        title,
        subject,
        priority,
        due_date
    )

    tasks.append(new_task.to_dict())

    save_data(TASK_FILE, tasks)

    print("\n✅ Task Added Successfully!")

# View all tasks
def view_tasks(student):

    tasks = load_data(TASK_FILE)

    print("\n========== MY TASKS ==========")

    found = False

    for task in tasks:

        if task["roll_number"] == student["roll_number"]:

            found = True

            print(f"\nTask ID    : {task['task_id']}")
            print(f"Title      : {task['title']}")
            print(f"Subject    : {task['subject']}")
            print(f"Priority   : {task['priority']}")
            print(f"Due Date   : {task['due_date']}")
            print(f"Status     : {task['status']}")

    if not found:
        print("\nNo Tasks Found.")

# Mark task as completed
def mark_task_completed(student):

    tasks = load_data(TASK_FILE)

    view_tasks(student)

    task_id = int(input("\nEnter Task ID to Complete : "))

    found = False

    for task in tasks:

        if (task["task_id"] == task_id and
                task["roll_number"] == student["roll_number"]):

            task["status"] = "Completed"
            found = True
            break

    if found:
        save_data(TASK_FILE, tasks)
        print("\n✅ Task Marked as Completed!")

    else:
        print("\n❌ Task Not Found!")

# Delete task
def delete_task(student):
    
    tasks = load_data(TASK_FILE)

    view_tasks(student)

    task_id = int(input("\nEnter Task ID to Delete : "))

    found = False

    for task in tasks:

        if (task["task_id"] == task_id and
                task["roll_number"] == student["roll_number"]):

            tasks.remove(task)
            found = True
            break

    if found:
        save_data(TASK_FILE, tasks)
        print("\n🗑️ Task Deleted Successfully!")

    else:
        print("\n❌ Task Not Found!")

# Edit task
def edit_task(student):

    tasks = load_data(TASK_FILE)

    view_tasks(student)

    task_id = int(input("\nEnter Task ID to Edit : "))

    found = False

    for task in tasks:

        if task["task_id"] == task_id and task["roll_number"] == student["roll_number"]:

            print("\nLeave blank if you don't want to change the value.")

            title = input(f"New Title ({task['title']}) : ")
            subject = input(f"New Subject ({task['subject']}) : ")
            priority = input(f"New Priority ({task['priority']}) : ")
            due_date = input(f"New Due Date ({task['due_date']}) : ")

            if title:
                task["title"] = title

            if subject:
                task["subject"] = subject

            if priority:
                task["priority"] = priority

            if due_date:
                task["due_date"] = due_date

            found = True
            break

    if found:
        save_data(TASK_FILE, tasks)
        print("\n✅ Task Updated Successfully!")

    else:
        print("\n❌ Task Not Found!")
    
def task_menu(student):

    while True:

        print("\n========== TASK MANAGER ==========")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task Completed")
        print("4. Edit Task")
        print("5. Delete Task")
        print("6. Back")

        choice = input("Enter Choice : ")

        if choice == "1":
            add_task(student)

        elif choice == "2":
            view_tasks(student)

        elif choice == "3":
            mark_task_completed(student)

        elif choice == "4":
            edit_task(student)

        elif choice == "5":
            delete_task(student)

        elif choice == "6":
            break

        else:
            print("Invalid Choice!")