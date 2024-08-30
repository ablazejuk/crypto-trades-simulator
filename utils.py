import requests
import json
import os

data_file = "crypto_data.json"
url = 'https://api.coingecko.com/api/v3/simple/price'
params = {'ids': 'bitcoin,ethereum,solana,sundog', 'vs_currencies': 'brl'}

class Utils:
    def __init__(self, gui):
        self.gui = gui

    def save_data(self):
        data = {"balance": self.gui.balance, "purchases": self.gui.purchases}
        with open(data_file, "w") as f:
            json.dump(data, f)
        print("Data saved.")

    def load_data(self):
        if os.path.exists(data_file):
            with open(data_file, "r") as f:
                data = json.load(f)
                self.gui.balance = data.get("balance", 100.0)
                self.gui.purchases = data.get("purchases", {})
                print("Data loaded.")
        else:
            self.gui.balance = 100.0
            self.gui.purchases = {'bitcoin': 0.0, 'ethereum': 0.0, 'solana': 0.0, 'sundog': 0.0}

    def fetch_crypto_prices(self):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            print("API Response:", data)
            self.gui.latest_prices.update(data)
        except requests.RequestException as e:
            print("Request Error:", e)

        self.update_prices()
        
        self.gui.root.after(60000, self.fetch_crypto_prices)

    def update_prices(self):
        self.gui.update_gui()

    def on_closing(self):
        self.save_data()
        self.gui.root.destroy()
