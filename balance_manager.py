from data_manager import DataManager
import inject
from singleton_metaclass import SingletonMeta

class BalanceManager(metaclass=SingletonMeta):
    INITIAL_BALANCE = 100.0

    @inject.autoparams()
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.balance = self.load_balance()

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

    def get_balance(self) -> float:
        return self.balance
    
    def reset_balance(self) -> None:
        self.balance = self.INITIAL_BALANCE
