import json
import os
from singleton_metaclass import SingletonMeta

class DataManager(metaclass=SingletonMeta):
    DATA_FILE = "crypto_data.json"

    def __init__(self):
        self.data = self.load_data()

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
