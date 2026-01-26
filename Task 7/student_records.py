import json

# Student records stored using dictionary
student_records = {
    101: {
        "name": "Saranya",
        "course": "Python Programming",
        "department": "CSE",
        "marks": 88,
        "attendance": 82
    },
    102: {
        "name": "Rahul",
        "course": "Artificial Intelligence",
        "department": "AI & DS",
        "marks": 92,
        "attendance": 90
    },
    103: {
        "name": "Neha",
        "course": "Data Science",
        "department": "CSE",
        "marks": 79,
        "attendance": 75
    }
}

print("\n📘 INITIAL STUDENT RECORDS")
print("-" * 35)
print(student_records)

# Accessing keys and values
print("\n🔍 ACCESSING INDIVIDUAL STUDENT DATA")
print("-" * 35)
print("Student Name (Roll 101):", student_records[101]["name"])
print("Marks (Roll 101):", student_records[101]["marks"])
print("Attendance (Roll 101):", student_records[101]["attendance"], "%")

# Updating and deleting entries
student_records[103]["marks"] = 85
student_records[103]["attendance"] = 80
del student_records[102]

print("\n✏️ UPDATED STUDENT RECORDS")
print("-" * 35)
print(student_records)

# Looping through dictionary
print("\n📋 DETAILED STUDENT REPORT")
print("-" * 35)
for roll_no, details in student_records.items():
    status = "Pass" if details["marks"] >= 40 else "Fail"
    eligibility = "Eligible" if details["attendance"] >= 75 else "Not Eligible"

    print(f"Roll No      : {roll_no}")
    print(f"Name         : {details['name']}")
    print(f"Department   : {details['department']}")
    print(f"Course       : {details['course']}")
    print(f"Marks        : {details['marks']}")
    print(f"Attendance   : {details['attendance']}%")
    print(f"Result       : {status}")
    print(f"Exam Status  : {eligibility}")
    print("-" * 35)

# Converting dictionary to JSON
json_data = json.dumps(student_records, indent=4)

# Saving JSON to file
with open("student_records.json", "w") as file:
    file.write(json_data)

print("\n💾 Student records successfully saved to student_records.json")

# Reading JSON back into Python
with open("student_records.json", "r") as file:
    loaded_records = json.load(file)

# Printing formatted output from JSON
print("\n📂 DATA READ FROM JSON FILE")
print("-" * 35)
for roll_no, details in loaded_records.items():
    print(f"[Roll No: {roll_no}] {details['name']} | {details['course']} | Marks: {details['marks']}")
