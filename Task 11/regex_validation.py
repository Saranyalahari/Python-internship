import re


# Regex Patterns (Centralized Validation Logic)

EMAIL_PATTERN = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
PHONE_PATTERN = r'^(?:\+91|91)?[6-9]\d{9}$'
PASSWORD_PATTERN = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'


# Validation Functions

def validate_email(email):
    if not email:
        return "❌ Email cannot be empty."
    if re.fullmatch(EMAIL_PATTERN, email):
        return "✅ Valid Email Address."
    return "❌ Invalid Email Format."


def validate_phone(phone):
    if not phone:
        return "❌ Phone number cannot be empty."
    if re.fullmatch(PHONE_PATTERN, phone):
        return "✅ Valid Indian Mobile Number."
    return "❌ Invalid Indian Mobile Number."


def validate_password(password):
    if not password:
        return "❌ Password cannot be empty."
    if re.fullmatch(PASSWORD_PATTERN, password):
        return "✅ Strong Password."
    return ("❌ Weak Password.\n"
            "Must be at least 8 characters long,\n"
            "include uppercase, lowercase, digit, and special character.")


# Main Program (Dynamic User Input)

def main():
    print("=== REGEX VALIDATION SYSTEM ===\n")

    email = input("Enter Email: ").strip()
    print(validate_email(email))

    print()

    phone = input("Enter Indian Mobile Number: ").strip()
    print(validate_phone(phone))

    print()

    password = input("Enter Password: ").strip()
    print(validate_password(password))


if __name__ == "__main__":
    main()
