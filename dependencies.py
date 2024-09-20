from balance_manager import BalanceManager
from balance_panel import BalancePanel
from coin_manager import CoinManager
from context_menu_manager import ContextMenuManager
from controls_panel import ControlsPanel
from data_manager import DataManager
from gui import GUI
from main_window import MainWindow
from purchase_manager import PurchaseManager
from table import Table

def configure_injections(binder):
    from app import App
    binder.bind_to_constructor(App, lambda: App())
    
    binder.bind_to_constructor(BalanceManager, lambda: BalanceManager())
    binder.bind_to_constructor(BalancePanel, lambda: BalancePanel())
    binder.bind_to_constructor(CoinManager, lambda: CoinManager())
    binder.bind_to_constructor(ContextMenuManager, lambda: ContextMenuManager())
    binder.bind_to_constructor(ControlsPanel, lambda: ControlsPanel())
    binder.bind_to_constructor(DataManager, lambda: DataManager())
    binder.bind_to_constructor(GUI, lambda: GUI())
    binder.bind_to_constructor(PurchaseManager, lambda: PurchaseManager())
    binder.bind_to_constructor(Table, lambda: Table())
    binder.bind_to_constructor(MainWindow, lambda: MainWindow())
