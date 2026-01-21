# grade_calculator.py
# This program calculates a student's grade based on marks and attendance

# Take marks input from the user
marks = int(input("Enter your marks (0–100): "))

# Take attendance input
attendance = input("Is attendance above 75%? (yes/no): ").lower()

# Validate marks
if marks < 0 or marks > 100:
    print("Invalid marks! Please enter a value between 0 and 100.")

else:
    # Nested condition for distinction
    if marks >= 90:
        if attendance == "yes":
            print("Grade: A+ (Distinction)")
        else:
            print("Grade: A")

    elif marks >= 75 and marks < 90:
        print("Grade: B")

    elif marks >= 60 and marks < 75:
        print("Grade: C")

    elif marks >= 40 and marks < 60:
        print("Grade: D")

    else:
        print("Grade: F (Fail)")
