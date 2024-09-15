from tkinter import Tk
from balance_panel import BalancePanel
from coin_manager import CoinManager
from context_menu_manager import ContextMenuManager
from controls_panel import ControlsPanel
from data_manager import DataManager
import inject
from balance_manager import BalanceManager
from purchase_manager import PurchaseManager
from singleton_metaclass import SingletonMeta
from table import Table

class GUI(metaclass=SingletonMeta):
    @inject.autoparams()
    def __init__(
        self, 
        balance_manager: BalanceManager, 
        purchase_manager: PurchaseManager, 
        coin_manager: CoinManager,
        data_manager: DataManager,
        context_menu_manager: ContextMenuManager,
        balance_panel: BalancePanel,
        controls_panel: ControlsPanel,
        table: Table
    ):
        self.balance_manager = balance_manager
        self.purchase_manager = purchase_manager
        self.coin_manager = coin_manager
        self.data_manager = data_manager
        self.balance_panel = balance_panel
        self.controls_panel = controls_panel
        self.table = table
        self.root = Tk()

        self.tree = self.create_main_window()
        context_menu_manager.setup_context_menu(self.root, self.tree)

        self.schedule_price_fetch()

        self.on_close()

    def schedule_price_fetch(self):
        self.coin_manager.fetch_crypto_prices()
        self.update_gui()
        self.root.after(60000, self.schedule_price_fetch)

    def run(self):
        self.root.mainloop()

    def on_close(self):
        def wrapper():
            balance = self.balance_manager.get_balance()
            purchases = self.purchase_manager.get_purchases()
            self.data_manager.save_data(balance, purchases)
            self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", wrapper)

    def create_main_window(self):
        self.root.title("Crypto Trades Simulator")
        self.root.geometry("900x600")

        self.balance_panel.create(self.root, self.reset_data)
        tree = self.table.create(self.root)
        self.controls_panel.create(self.root, self.update_gui)

        return tree

    def reset_data(self):
        self.balance_manager.reset_balance()
        self.purchase_manager.reset_purchases()
        self.update_gui()

    def update_gui(self):
        self.balance_panel.update()
        self.table.update()
