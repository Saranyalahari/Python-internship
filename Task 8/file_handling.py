import csv

# TEXT FILE OPERATIONS

try:
    # 1 & 2. Create text file and write user data
    with open("users.txt", "w") as file:
        name = input("Enter your name: ")
        role = input("Enter your role: ")
        file.write(f"Name: {name}\n")
        file.write(f"Role: {role}\n")

    print("\n✅ Data written to users.txt")

    # 3. Read file contents
    print("\n📖 Reading users.txt:")
    with open("users.txt", "r") as file:
        print(file.read())

    # 4. Append data to file
    with open("users.txt", "a") as file:
        file.write("Status: Active\n")

    print("✅ Data appended to users.txt")

except FileNotFoundError:
    print("❌ File not found error occurred.")
except IOError:
    print("❌ File input/output error occurred.")

# CSV FILE OPERATIONS

try:
    # 6. Create CSV file using csv module
    with open("students.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)

        # Write header
        writer.writerow(["Roll No", "Name", "Marks"])

        # 7. Write multiple rows
        writer.writerow([101, "Saranya", 88])
        writer.writerow([102, "Rahul", 92])
        writer.writerow([103, "Neha", 85])

    print("\n✅ students.csv created and data written")

    # 8. Read CSV data
    print("\n📊 Reading students.csv:")
    with open("students.csv", "r") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            print(row)

except Exception as e:
    print("❌ Error while handling CSV file:", e)

