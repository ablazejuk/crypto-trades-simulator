import json
import os

class DataManager:
    DATA_FILE = "crypto_data.json"
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance
    
    def __init__(self):
        if not self.__initialized:
            self.data = self.load_data()
            self.__initialized = True

    def load_data(self):
        if not os.path.exists(self.DATA_FILE):
            return None
        
        with open(self.DATA_FILE, "r") as file:
            return json.load(file)

    def get_value(self, key):
        if self.data and key in self.data:
            return self.data[key]
        
        return None

    def save_data(self, balance, purchases):
        data = {
            "balance": balance,
            "purchases": purchases
        }

        with open(self.DATA_FILE, "w") as f:
            json.dump(data, f)
        
        print("Data saved.")
