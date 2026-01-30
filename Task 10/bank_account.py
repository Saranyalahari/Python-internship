# Base class
class BankAccount:
    def __init__(self, account_number, holder_name, balance=0):
        # Encapsulation: protected attributes
        self._account_number = account_number
        self._holder_name = holder_name
        self._balance = balance

    # Getter methods
    def get_account_number(self):
        return self._account_number

    def get_holder_name(self):
        return self._holder_name

    def get_balance(self):
        return self._balance

    # Bank operations
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print(f"₹{amount} deposited successfully.")
        else:
            print("Invalid deposit amount.")

    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid withdrawal amount.")
        elif amount > self._balance:
            print("Insufficient balance.")
        else:
            self._balance -= amount
            print(f"₹{amount} withdrawn successfully.")

    # Method to be overridden
    def account_type(self):
        return "Generic Bank Account"


# Savings Account class
class SavingsAccount(BankAccount):
    def __init__(self, account_number, holder_name, balance=0, interest_rate=4):
        super().__init__(account_number, holder_name, balance)
        self.interest_rate = interest_rate

    # Overriding method
    def account_type(self):
        return "Savings Account"

    def add_interest(self):
        interest = (self._balance * self.interest_rate) / 100
        self._balance += interest
        print(f"Interest ₹{interest} added.")


# Current Account class
class CurrentAccount(BankAccount):
    def __init__(self, account_number, holder_name, balance=0, overdraft_limit=10000):
        super().__init__(account_number, holder_name, balance)
        self.overdraft_limit = overdraft_limit

    # Overriding method
    def account_type(self):
        return "Current Account"

    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid withdrawal amount.")
        elif amount > self._balance + self.overdraft_limit:
            print("Overdraft limit exceeded.")
        else:
            self._balance -= amount
            print(f"₹{amount} withdrawn successfully (Overdraft allowed).")


# Main Program: Creating Objects & Simulating Banking

account1 = SavingsAccount(101, "Saranya", 5000)
account2 = CurrentAccount(102, "Rahul", 10000)

print("\n--- Account Details ---")
print(account1.get_holder_name(), "-", account1.account_type())
print(account2.get_holder_name(), "-", account2.account_type())

print("\n--- Transactions ---")
account1.deposit(2000)
account1.add_interest()
account1.withdraw(3000)

account2.withdraw(15000)
account2.deposit(5000)

print("\n--- Final Balances ---")
print(f"{account1.get_holder_name()} Balance: ₹{account1.get_balance()}")
print(f"{account2.get_holder_name()} Balance: ₹{account2.get_balance()}")
