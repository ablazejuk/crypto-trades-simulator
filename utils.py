from coin_manager import CoinManager
import inject
import requests
import json

data_file = "crypto_data.json"
url = 'https://api.coingecko.com/api/v3/simple/price'
params = {'ids': 'bitcoin,ethereum,solana,sundog', 'vs_currencies': 'brl'}

class Utils:
    @inject.autoparams()
    def __init__(self, coin_manager: CoinManager, gui):
        self.coin_manager = coin_manager
        self.gui = gui

    def save_data(self):
        data = {"balance": self.gui.balance_manager.get_balance(), "purchases": self.gui.purchase_manager.get_purchases()}
        with open(data_file, "w") as f:
            json.dump(data, f)
        print("Data saved.")

    def fetch_crypto_prices(self):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            print("API Response:", data)
            self.coin_manager.set_latest_prices(data)
        except requests.RequestException as e:
            print("Request Error:", e)

        self.gui.update_gui()
        self.gui.root.after(60000, self.fetch_crypto_prices)

    def on_closing(self):
        self.save_data()
        self.gui.root.destroy()
