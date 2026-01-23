# 2. Store student names in a list
students = ["Saranya", "Rahul", "Anita", "Rahul", "Kiran"]

print("\nInitial Student List:")
print(students)

# 3. Add, remove, and sort elements in the list
students.append("Neha")
students.remove("Anita")
students.sort()

print("\nUpdated Student List:")
for i, name in enumerate(students, start=1):
    print(f"{i}. {name}")

# 4. Use tuple to store fixed data
course_info = ("Python Programming", "Internship", 6)

print("\nCourse Information:")
print(f"Course Name : {course_info[0]}")
print(f"Type        : {course_info[1]}")
print(f"Duration    : {course_info[2]} Weeks")

# 5. Convert list to set to remove duplicate student names
unique_students = set(students)

print("\nUnique Students:")
for name in sorted(unique_students):
    print(f"- {name}")

# 6. Perform set operations
offline_students = {"Rahul", "Kiran"}
online_students = {"Saranya", "Neha", "Kiran"}

print("\nSet Operations Results:")
print("All Students        :", sorted(unique_students | online_students))
print("Online & Enrolled   :", sorted(unique_students & online_students))
print("Offline Only        :", sorted(offline_students - online_students))

# 7. Iterate over collections and display status
print("\nIteration Examples:")
for name in students:
    status = "Online" if name in online_students else "Offline"
    print(f"{name:<10} : {status}")

# 8. Compare mutable (list) and immutable (tuple)
students[0] = students[0].upper()
print("\nMutable vs Immutable:")
print("Modified List       :", students)
print("Tuple remains same  :", course_info)

# 9. Print formatted output
print("\nFinal Formatted Output:")
for idx, name in enumerate(unique_students, start=101):
    print(f"Student ID: {idx} | Name: {name}")
