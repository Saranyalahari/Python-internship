# This program demonstrates different data types in Python

# --------------------------------------------------
# 1 & 2. Declare variables of different data types
# --------------------------------------------------
age = 21                 # int
height = 5.6             # float
name = "Saranya"         # string
is_student = True        # boolean

# --------------------------------------------------
# 3. Print the type of each variable
# --------------------------------------------------
print("Data Types:")
print("age:", type(age))
print("height:", type(height))
print("name:", type(name))
print("is_student:", type(is_student))

print("\n-----------------------------------")

# --------------------------------------------------
# 4. Arithmetic operations using numeric variables
# --------------------------------------------------
sum_value = age + 5
product_value = age * 2
division_value = height / 2

print("Arithmetic Operations:")
print("Sum:", sum_value)
print("Product:", product_value)
print("Division:", division_value)

print("\n-----------------------------------")

# --------------------------------------------------
# 5 & 6. Type casting with error handling
# --------------------------------------------------
try:
    number_str = input("Enter a number: ")

    int_value = int(number_str)
    float_value = float(number_str)

    print("Integer value:", int_value)
    print("Float value:", float_value)

except ValueError:
    print("Invalid input! Please enter a numeric value.")

print("\n-----------------------------------")

# --------------------------------------------------
# 7. Concatenate strings and numbers properly
# --------------------------------------------------
print("String and Number Concatenation:")
print("Name: " + name + ", Age: " + str(age))

print("\n-----------------------------------")

# --------------------------------------------------
# 8. Demonstrate dynamic typing
# --------------------------------------------------
value = 10
print("Value:", value, "Type:", type(value))

value = "Now I am a string"
print("Value:", value, "Type:", type(value))
