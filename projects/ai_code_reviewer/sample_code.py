import math

def calculate(a,b):
    if a>0 and b>0:
        result=a+b
    else:
        result = a - b
    return result

def factorial(n):
    if n==0:
        return 1
    else:
        return n*factorial(n-1)

def complex_function(x):
    if x > 0:
        if x % 2 == 0:
            if x > 10:
                return x * 2
            else:
                return x + 2
        else:
            if x > 5:
                return x - 2
            else:
                return x + 1
    else:
        return 0

print(calculate(5,3))
print(factorial(5))
print(complex_function(12))