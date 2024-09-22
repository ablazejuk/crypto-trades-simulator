from tkinter import Tk
from coin_manager import CoinManager
from context_menu_manager import ContextMenuManager
from data_manager import DataManager
import inject
from balance_manager import BalanceManager
from main_window import MainWindow
from purchase_manager import PurchaseManager
from singleton_metaclass import SingletonMeta

class GUI(metaclass=SingletonMeta):
    @inject.autoparams()
    def __init__(
        self, 
        balance_manager: BalanceManager, 
        purchase_manager: PurchaseManager, 
        coin_manager: CoinManager,
        data_manager: DataManager,
        context_menu_manager: ContextMenuManager,
        main_window: MainWindow
    ) -> None:
        self.balance_manager = balance_manager
        self.purchase_manager = purchase_manager
        self.coin_manager = coin_manager
        self.data_manager = data_manager
        self.main_window = main_window
        self.root = Tk()

        self.tree = self.main_window.create(self.root)
        context_menu_manager.setup_context_menu(self.root, self.tree)

        self.schedule_price_fetch()

        self.on_close()

    def schedule_price_fetch(self) -> None:
        self.coin_manager.fetch_crypto_prices()
        self.main_window.update()
        self.root.after(60000, self.schedule_price_fetch)

    def run(self) -> None:
        self.root.mainloop()

    def on_close(self) -> None:
        def wrapper() -> None:
            balance = self.balance_manager.get_balance()
            purchases = self.purchase_manager.get_purchases()
            self.data_manager.save_data(balance, purchases)
            self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", wrapper)
