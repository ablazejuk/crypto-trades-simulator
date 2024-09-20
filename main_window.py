from balance_manager import BalanceManager
from balance_panel import BalancePanel
from controls_panel import ControlsPanel
import inject
from purchase_manager import PurchaseManager
from singleton_metaclass import SingletonMeta
from table import Table

class MainWindow(metaclass=SingletonMeta):
    @inject.autoparams()
    def __init__(
        self, 
        balance_panel: BalancePanel,
        table: Table,
        controls_panel: ControlsPanel,
        balance_manager: BalanceManager,
        purchase_manager: PurchaseManager
    ):
        self.balance_panel = balance_panel
        self.table = table
        self.controls_panel = controls_panel
        self.balance_manager = balance_manager
        self.purchase_manager = purchase_manager

    def create(self, root):
        self.root = root
        self.root.title("Crypto Trades Simulator")
        self.root.geometry("900x600")

        self.balance_panel.create(self.root, self.reset_data)
        self.tree = self.table.create(self.root)
        self.controls_panel.create(self.root, self.update)

        return self.tree

    def update(self):
        self.balance_panel.update()
        self.table.update()

    def reset_data(self):
        self.balance_manager.reset_balance()
        self.purchase_manager.reset_purchases()
        self.update()