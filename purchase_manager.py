import os
import json
from balance_manager import BalanceManager
from coin_manager import CoinManager
import inject
import copy

class PurchaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    @inject.autoparams()
    def __init__(self, balance_manager: BalanceManager, coin_manager: CoinManager):
        if not self.__initialized:
            self.balance_manager = balance_manager
            self.coin_manager = coin_manager
            self.initial_purchases = {coin: 0.0 for coin in coin_manager.get_available_coins()}
            self.latest_prices = {}
            self.purchases = self.load_purchases()
            self.__initialized = True

    def load_purchases(self):
        data_file = "crypto_data.json"

        if not os.path.exists(data_file):
            return self.initial_purchases

        with open(data_file, "r") as file:
            data = json.load(file)
            return data.get('purchases', self.initial_purchases)

    def buy_crypto(self, crypto, amount):
        try:
            price = self.coin_manager.get_latest_prices()[crypto]['brl']
            quantity = round(amount / price, 8)

            self.balance_manager.deduct_funds(amount)
            self.purchases[crypto] = round(self.purchases.get(crypto, 0) + quantity, 8)

            return f"Bought {quantity:.8f} {crypto.capitalize()} for {amount:.2f} BRL."
        except KeyError:
            return "Invalid cryptocurrency selected."
        except ValueError:
            return "Invalid amount entered."

    def sell_crypto(self, crypto, amount):
        try:
            price = self.coin_manager.get_latest_prices()[crypto]['brl']
            quantity = round(amount / price, 8)

            if self.purchases.get(crypto, 0) >= quantity:
                self.purchases[crypto] = round(self.purchases[crypto] - quantity, 8)
                self.balance_manager.add_funds(amount)

                return f"Sold {quantity:.8f} {crypto.capitalize()} for {amount:.2f} BRL."
            else:
                return "Insufficient cryptocurrency to sell."
        except KeyError:
            return "Invalid cryptocurrency selected."
        except ValueError:
            return "Invalid amount entered."

    def get_purchases(self):
        return self.purchases

    def reset_purchases(self):
        self.purchases = copy.deepcopy(self.initial_purchases)
