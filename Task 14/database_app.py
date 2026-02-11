import sqlite3

# Connect to SQLite Database

def connect_db():
    conn = sqlite3.connect("students.db")
    return conn

# Create Table

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            marks INTEGER NOT NULL
        )
    """)
    conn.commit()

# Insert Record (Parameterized Query)

def insert_student(conn, name, email, marks):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO students (name, email, marks) VALUES (?, ?, ?)",
            (name, email, marks)
        )
        conn.commit()
        print("✅ Student inserted successfully.")
    except sqlite3.IntegrityError:
        print("❌ Email already exists.")

# Fetch Records

def fetch_students(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    print("\n--- Student Records ---")
    print("-" * 40)
    for row in rows:
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Email: {row[2]}")
        print(f"Marks: {row[3]}")
        print("-" * 40)

# Update Record

def update_marks(conn, student_id, new_marks):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE students SET marks = ? WHERE id = ?",
        (new_marks, student_id)
    )
    conn.commit()
    print("✅ Marks updated successfully.")


# Delete Record

def delete_student(conn, student_id):
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )
    conn.commit()
    print("✅ Student deleted successfully.")

# Main Program

def main():
    conn = connect_db()
    create_table(conn)

    while True:
        print("\n=== Student Database Menu ===")
        print("1. Insert Student")
        print("2. View Students")
        print("3. Update Marks")
        print("4. Delete Student")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter Name: ")
            email = input("Enter Email: ")
            marks = int(input("Enter Marks: "))
            insert_student(conn, name, email, marks)

        elif choice == "2":
            fetch_students(conn)

        elif choice == "3":
            student_id = int(input("Enter Student ID: "))
            new_marks = int(input("Enter New Marks: "))
            update_marks(conn, student_id, new_marks)

        elif choice == "4":
            student_id = int(input("Enter Student ID: "))
            delete_student(conn, student_id)

        elif choice == "5":
            print("Closing database connection...")
            conn.close()
            break

        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    main()
