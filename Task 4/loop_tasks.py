# This program demonstrates different loop concepts in Python

# 1. FOR loop to print numbers from 1 to 100
# Real-world example: Printing roll numbers of students
# --------------------------------------------------
print("Numbers from 1 to 100:")
for number in range(1, 101):
    print(number, end=" ")

print("\n")

# --------------------------------------------------
# 2. WHILE loop for countdown timer
# Real-world example: Countdown before an exam starts
# --------------------------------------------------
countdown = 10

print("Countdown Timer:")
while countdown > 0:
    print(countdown)
    countdown -= 1

print("Time's up!")

print("\n")

# --------------------------------------------------
# 3. Using BREAK and CONTINUE
# Real-world example: Skip break time, stop at closing time
# --------------------------------------------------
print("Working hours simulation:")

for hour in range(1, 9):
    if hour == 4:
        continue  # Skip break hour
    if hour == 8:
        break     # Stop work at closing time
    print(f"Working hour: {hour}")

print("\n")

# --------------------------------------------------
# 4. Iterate over string characters
# Real-world example: Checking characters in a username
# --------------------------------------------------
username = "Saranya"

print("Characters in username:")
for char in username:
    print(char)

print("\n")

# --------------------------------------------------
# 5. Generate multiplication table
# Real-world example: Learning tables in school
# --------------------------------------------------
num = 5
print(f"Multiplication Table of {num}:")

for i in range(1, 11):
    print(f"{num} x {i} = {num * i}")

print("\n-----------------------------------")

# --------------------------------------------------
# 6. Using range with steps
# Real-world example: Printing even numbers
# --------------------------------------------------
print("Even numbers from 2 to 20:")
for even in range(2, 21, 2):
    print(even, end=" ")

print("\n\n")

# --------------------------------------------------
# 7. Combining loops with conditions
# Real-world example: Checking pass/fail status
# --------------------------------------------------
marks_list = [35, 78, 90, 42, 55]

print("Pass/Fail Status:")
for marks in marks_list:
    if marks >= 40:
        print(marks, "- Pass")
    else:
        print(marks, "- Fail")
