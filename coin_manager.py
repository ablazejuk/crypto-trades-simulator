import requests
from singleton_metaclass import SingletonMeta

class CoinManager(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.available_coins = ["bitcoin", "ethereum", "solana", "sundog"]
        self.latest_prices = {}

    def get_available_coins(self):
        return self.available_coins
    
    def get_latest_prices(self):
        return self.latest_prices
    
    def fetch_crypto_prices(self) -> None:
        try:
            url = 'https://api.coingecko.com/api/v3/simple/price'
            params = {
                'ids': ',' . join(self.get_available_coins()),
                'vs_currencies': 'brl'
            }
            response = requests.get(url, params)
            response.raise_for_status()
            data = response.json()
            print("API Response:", data)
            self.latest_prices = data
        except requests.RequestException as e:
            print("Request Error:", e)
