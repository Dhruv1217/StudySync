from student import create_account
from student import create_account, login, student_dashboard

while True:

    print("\n========== STUDYSYNC ==========")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter Choice (1,2 or 3) : ")

    if choice == "1":
        create_account()

    elif choice == "2":

        user = login()

        if user:
            student_dashboard(user)

    elif choice == "3":
        print("Thank You!")
        break

    else:
        print("Invalid Choice")

