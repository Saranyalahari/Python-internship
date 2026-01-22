# --------------------------------------------------
# Arithmetic Functions
# --------------------------------------------------

def add(a, b=0):
    """Return the sum of two numbers."""
    return a + b


def subtract(a, b=0):
    """Return the difference of two numbers."""
    return a - b


def multiply(a, b=1):
    """Return the product of two numbers."""
    return a * b


def divide(a, b=1):
    """
    Return the division of two numbers.
    Handles division by zero safely.
    """
    if b == 0:
        return None
    return a / b


# --------------------------------------------------
# Input & Utility Functions
# --------------------------------------------------

def get_numbers():
    """Get two numeric inputs from the user."""
    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        return num1, num2
    except ValueError:
        print("❌ Invalid input! Please enter numbers only.")
        return None, None


def show_menu():
    """Display calculator options."""
    print("\n========== Calculator ==========")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Exit")
    print("================================")


def process_choice(choice):
    """Process user choice and call corresponding function."""
    num1, num2 = get_numbers()
    if num1 is None or num2 is None:
        return

    if choice == "1":
        print("✅ Result:", add(num1, num2))

    elif choice == "2":
        print("✅ Result:", subtract(num1, num2))

    elif choice == "3":
        print("✅ Result:", multiply(num1, num2))

    elif choice == "4":
        result = divide(num1, num2)
        if result is None:
            print("❌ Error: Division by zero is not allowed.")
        else:
            print("✅ Result:", result)


# --------------------------------------------------
# Main Program Controller
# --------------------------------------------------

def main():
    """Main function controlling program flow."""
    while True:
        show_menu()
        choice = input("Enter your choice (1–5): ")

        if choice == "5":
            print("👋 Calculator closed. Thank you!")
            break

        elif choice in ["1", "2", "3", "4"]:
            process_choice(choice)

        else:
            print("❌ Invalid choice! Please select between 1 and 5.")


# --------------------------------------------------
# Program Entry Point
# --------------------------------------------------

if __name__ == "__main__":
    main()
