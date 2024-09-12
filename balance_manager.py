from data_manager import DataManager
import inject

class BalanceManager:
    _instance = None
    INITIAL_BALANCE = 100.0

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    @inject.autoparams()
    def __init__(self, data_manager: DataManager):
        if not self.__initialized:
            self.data_manager = data_manager
            self.balance = self.load_balance()
            self.__initialized = True

    def load_balance(self):
        balance = self.data_manager.get_value('balance')

        if not balance:
            return self.INITIAL_BALANCE
        
        return balance

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
