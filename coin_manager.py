class CoinManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CoinManager, cls).__new__(cls)
            cls._instance.available_coins = ["bitcoin", "ethereum", "solana", "sundog"]
            cls._instance.latest_prices = {}
        return cls._instance

    def get_available_coins(self):
        return self.available_coins
    
    def set_latest_prices(self, latest_prices):
        self.latest_prices = latest_prices

    def get_latest_prices(self):
        return self.latest_prices
