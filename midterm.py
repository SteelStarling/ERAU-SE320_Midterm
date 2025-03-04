"""Code for the SE320 Midterm Exam Assignment
Author: Taylor Hancock
        Editing code by Wolf Paulus
Date:   03/03/2025
Class:  SE320 - Software Construction
Assignment: Midterm Exam Assignment
"""

import functools
from typing import List, Self

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
    def wrapper(self, amount, *args, **kwargs):
        # check if out of bounds
        if amount < 0:
            raise ValueError("Negative amount invalid")
        if amount >= 1000:
            raise ValueError("Transaction too large")

        # return function response
        return func(self, amount, *args, **kwargs)
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
    
    @validate_amount # prevents being given an invalid amount initially
    def transfer_funds(self, amount: float, targetAccount: Self) -> None:
        """Transfers funds from the specified account into the target account
        amount: how much money to transfer
        targetAccount: the account to transfer the money to
        """

        # Attempt to withdraw money (otherwise it crashes out)
        self.withdraw(amount)

        # if successful, deposit money
        try:
            targetAccount.deposit(amount)
        except Exception as e:
            print(f"Transfer failed: {e}")
            self.deposit(amount)

        """with how this is setup, it will never fail to deposit, but,
        for completeness's sake, I'm adding code to handle a failure,
        as I figured it could be fun. In the case of failure, it will
        simply try once to deposit the money back in the account, and
        if it crashes out, it will break (not good for a real banking
        system, but good enough for this assignment, I presume)"""


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

    account_b = BankAccount("00001", "Jane Roe")

    account_b.deposit(400)

    try:
        account_b.transfer_funds(600, account)   # Should fail (insufficient funds)
    except ValueError as e:
        print(f"Transfer failed: {e}")

    try:
        account_b.transfer_funds(1000, account)   # Should fail (over 1000)
    except ValueError as e:
        print(f"Transfer failed: {e}")

    account_b.transfer_funds(200, account)   # Should succeed

    # Print history
    print(account.get_transaction_history())
    print(account_b.get_transaction_history())
