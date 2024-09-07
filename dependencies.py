from balance_manager import BalanceManager
from coin_manager import CoinManager
from purchase_manager import PurchaseManager

def configure_injections(binder):
    balance_manager_instance = BalanceManager()
    binder.bind(BalanceManager, balance_manager_instance)

    coin_manager_instance = CoinManager()
    binder.bind(CoinManager, coin_manager_instance)
    binder.bind(PurchaseManager, PurchaseManager(balance_manager_instance, coin_manager_instance))
