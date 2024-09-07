from balance_manager import BalanceManager
from coin_manager import CoinManager
from gui import GUI
from purchase_manager import PurchaseManager

def configure_injections(binder):
    binder.bind_to_constructor(BalanceManager, lambda: BalanceManager())
    binder.bind_to_constructor(CoinManager, lambda: CoinManager())
    binder.bind_to_constructor(PurchaseManager, lambda: PurchaseManager())
    binder.bind_to_constructor(GUI, lambda: GUI())
