from file_handler import load_data, save_data

CGPA_FILE = "data/cgpa.json"

# Calculate CGPA
def calculate_cgpa(student):
    
    cgpa_data = load_data(CGPA_FILE)

    print("\n========== CGPA CALCULATOR ==========")

    while True:
        try:
            total_semesters = int(input("Enter Total Semesters Completed (1-8) : "))
            if 1 <= total_semesters <= 8:
                break
            else:
                print("❌ Total semesters must be between 1 and 8.")
        except ValueError:
            print("❌ Enter a valid integer.")

    total_sgpa = 0

    semester_list = []

    for i in range(1, total_semesters + 1):

        while True:
            try:
                sgpa = float(input(f"Enter SGPA of Semester {i} : "))

                if 0 <= sgpa <= 10:
                    semester_list.append(sgpa)
                    break
                else:
                    print("❌ SGPA should be between 0 and 10.")

            except ValueError:
                print("❌ Enter a valid number.")

        total_sgpa += sgpa

    cgpa = total_sgpa / total_semesters

    record = {
        "roll_number": student["roll_number"],
        "semester_sgpa": semester_list,
        "cgpa": round(cgpa, 2)
    }

    found = False

    for data in cgpa_data:

        if data["roll_number"] == student["roll_number"]:

            data.update(record)

            found = True

            break

    if not found:

        cgpa_data.append(record)

    save_data(CGPA_FILE, cgpa_data)

    print("\n========== RESULT ==========")

    print(f"CGPA : {cgpa:.2f}")