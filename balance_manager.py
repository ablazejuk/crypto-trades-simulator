import os
import json

class BalanceManager:
    _instance = None
    INITIAL_BALANCE = 100.0

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if not self.__initialized:
            self.balance = self.load_balance()
            self.__initialized = True

    def load_balance(self):
        data_file = "crypto_data.json"

        if not os.path.exists(data_file):
            return self.INITIAL_BALANCE

        with open(data_file, "r") as file:
            data = json.load(file)
            return data.get('balance', self.INITIAL_BALANCE)

    def add_funds(self, amount):
        self.balance += amount

    def deduct_funds(self, amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            raise ValueError("Insufficient balance")

    def get_balance(self):
        return self.balance
    
    def reset_balance(self):
        self.balance = self.INITIAL_BALANCE
