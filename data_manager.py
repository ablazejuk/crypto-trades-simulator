import json
from balance_manager import BalanceManager
import inject
from purchase_manager import PurchaseManager

class DataManager:
    DATA_FILE = "crypto_data.json"
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance
    
    @inject.autoparams()
    def __init__(self, balance_manager: BalanceManager, purchase_manager: PurchaseManager):
        if not self.__initialized:
            self.balance_manager = balance_manager
            self.purchase_manager = purchase_manager
            self.__initialized = True

    def save_data(self):
        balance = self.balance_manager.get_balance()
        purchases = self.purchase_manager.get_purchases()
        data = {
            "balance": balance,
            "purchases": purchases
        }

        with open(self.DATA_FILE, "w") as f:
            json.dump(data, f)
        
        print("Data saved.")
