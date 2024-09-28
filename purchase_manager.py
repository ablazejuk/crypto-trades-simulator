from balance_manager import BalanceManager
from coin_manager import CoinManager
from data_manager import DataManager
import inject
import copy
from singleton_metaclass import SingletonMeta

class PurchaseManager(metaclass=SingletonMeta):

    @inject.autoparams()
    def __init__(self, balance_manager: BalanceManager, coin_manager: CoinManager, data_manager: DataManager):
        self.balance_manager = balance_manager
        self.coin_manager = coin_manager
        self.data_manager = data_manager
        self.initial_purchases = {coin: 0.0 for coin in coin_manager.get_available_coins()}
        self.purchases: dict[str, float] = self.load_purchases()

    def load_purchases(self) -> dict[str, float]:
        purchases: dict[str, float] = self.data_manager.get_value('purchases')

        if not purchases:
            return self.initial_purchases
        
        return purchases

    def buy_crypto(self, crypto: str, amount: float) -> str:
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

    def sell_crypto(self, crypto: str, amount: float) -> str:
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

    def get_purchases(self) -> dict[str, float]:
        return self.purchases

    def reset_purchases(self) -> None:
        self.purchases = copy.deepcopy(self.initial_purchases)
