import logging

# Logging Configuration
logging.basicConfig(
    filename="error_log.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

print("=== Error Handling Demonstration Program ===\n")


# Function to simulate runtime errors
def perform_operations():
    try:
        # Simulate ValueError
        number = int(input("Enter an integer number: "))

        # Simulate ZeroDivisionError
        result = 100 / number

        # Simulate TypeError
        text = "Python"
        final_value = text + result

        print("Final Value:", final_value)

    except ValueError as ve:
        logging.error("ValueError occurred: Invalid integer input", exc_info=True)
        print("❌ Error: Please enter a valid integer.")

    except ZeroDivisionError as zde:
        logging.error("ZeroDivisionError occurred: Division by zero", exc_info=True)
        print("❌ Error: Division by zero is not allowed.")

    except TypeError as te:
        logging.error("TypeError occurred: Type mismatch", exc_info=True)
        print("❌ Error: Invalid operation between different data types.")

    except Exception as e:
        logging.error("Unexpected error occurred", exc_info=True)
        print("❌ Error: An unexpected error occurred.")

    else:
        print("✅ Operation completed successfully without errors.")

    finally:
        print("🔍 Execution completed. Check log file for details.\n")


# Program Execution

perform_operations()
