class CoinManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if not self.__initialized:
            self.available_coins = ["bitcoin", "ethereum", "solana", "sundog"]
            self.latest_prices = {}
            self.__initialized = True

    def get_available_coins(self):
        return self.available_coins
    
    def set_latest_prices(self, latest_prices):
        self.latest_prices = latest_prices

    def get_latest_prices(self):
        return self.latest_prices
