"""Code for the SE320 Midterm Exam Assignment
Author: Taylor Hancock, editing code by Wolf Paulus
Date:   03/03/2025
Class:  SE320 - Software Construction
Assignment: Midterm Exam Assignment
"""

import functools
from typing import List

def log_transaction(func: callable) -> callable:
    """Logs any transaction that changes the account balance"""
    @functools.wraps(func)
    def wrapper(self, amount):
        initial_balance = self.balance
        result = func(self, amount)
        print(f"Transaction: {func.__name__}, Amount: ${amount}, "
              f"Balance: ${self.balance}")
        return result
    return wrapper

def validate_amount(func: callable) -> callable:
    """Decorator that validates the amount parameter:
    - Must be positive number
    - Must be less than $1000
      raises a ValueError is validation fails
    """
    @functools.wraps(func)
    def wrapper(self, amount):
        # check if out of bounds
        if amount < 0:
            raise ValueError("Negative amount invalid")
        if amount >= 1000:
            raise ValueError("Transaction too large")

        # return function response
        return func(self, amount)
    return wrapper


class BankAccount:
    """Stores a series of transactions for a given bank account
    account_number: String for the account number
    owner_name:     Name of the account owner
    balance:        Total account balance
    transactions:   List of all transactions taken
    """

    def __init__(self, account_number: str, owner_name: str):
        """Creates a new BankAccount to handle transactions"""
        self.account_number = account_number
        self.owner_name = owner_name
        self.balance = 0
        self.transactions: List[str] = []

    @validate_amount
    @log_transaction
    def deposit(self, amount: float) -> None:
        """Add money to account"""
        self.balance += amount
        self.transactions.append(f"Deposit: ${amount}")

    @validate_amount
    @log_transaction
    def withdraw(self, amount: float) -> None:
        """Remove money from account if sufficient funds exist"""
        if self.balance >= amount:
            self.balance -= amount
            self.transactions.append(f"Withdrawal: ${amount}")
        else:
            raise ValueError("Insufficient funds")

    def get_transaction_history(self) -> List[str]:
        """Return list of all transactions"""
        return self.transactions


if __name__ == "__main__":
    # Example test cases from Assignment:

    # Create account
    account = BankAccount("12345", "John Doe")

    # Test transactions
    account.deposit(500)    # Should work
    account.withdraw(200)   # Should work
    try:
        account.deposit(1500)   # Should fail (over $1000)
    except ValueError as e:
        print(f"Deposit failed: {e}")

    try:
        account.withdraw(400)   # Should fail (insufficient funds)
    except ValueError as e:
        print(f"Withdraw failed: {e}")

    # Print history
    print(account.get_transaction_history())
