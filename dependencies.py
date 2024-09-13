from balance_manager import BalanceManager
from coin_manager import CoinManager
from context_menu_manager import ContextMenuManager
from data_manager import DataManager
from gui import GUI
from purchase_manager import PurchaseManager

def configure_injections(binder):
    from app import App
    binder.bind_to_constructor(App, lambda: App())
    
    binder.bind_to_constructor(BalanceManager, lambda: BalanceManager())
    binder.bind_to_constructor(CoinManager, lambda: CoinManager())
    binder.bind_to_constructor(ContextMenuManager, lambda: ContextMenuManager())
    binder.bind_to_constructor(DataManager, lambda: DataManager())
    binder.bind_to_constructor(GUI, lambda: GUI())
    binder.bind_to_constructor(PurchaseManager, lambda: PurchaseManager())
