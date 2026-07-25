from file_handler import load_data, save_data
ATTENDANCE_FILE = "data/attendance.json"

def attendance_calculator(student):

    attendance_data = load_data(ATTENDANCE_FILE)

    print("\n========== ATTENDANCE ==========")

    while True:
        try:
            total_classes = int(input("Enter Total Classes : "))
            attended_classes = int(input("Enter Attended Classes : "))

            if total_classes <= 0:
                print("❌ Total classes must be greater than 0.")
                continue

            if attended_classes < 0 or attended_classes > total_classes:
                print("❌ Invalid attended classes.")
                continue

            break

        except ValueError:
            print("❌ Please enter numbers only.")

    percentage = (attended_classes / total_classes) * 100

    record = {
        "roll_number": student["roll_number"],
        "total_classes": total_classes,
        "attended_classes": attended_classes,
        "attendance_percentage": round(percentage, 2)
    }

    found = False

    for data in attendance_data:
        if data["roll_number"] == student["roll_number"]:
            data.update(record)
            found = True
            break

    if not found:
        attendance_data.append(record)

    save_data(ATTENDANCE_FILE, attendance_data)

    print(f"\nAttendance : {percentage:.2f}%")

    if percentage >= 75:
        print("Status : Eligible ✅")
    else:
        print("Status : Short Attendance ❌")