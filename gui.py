from tkinter import Frame, Label, Entry, Tk, ttk
from balance_panel import BalancePanel
from coin_manager import CoinManager
from context_menu_manager import ContextMenuManager
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
        table: Table
    ):
        self.balance_manager = balance_manager
        self.purchase_manager = purchase_manager
        self.coin_manager = coin_manager
        self.data_manager = data_manager
        self.balance_panel = balance_panel
        self.table = table
        self.root = Tk()

        self.tree, self.controls_frame, self.amount_entry = self.create_main_window()

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

        controls_frame = Frame(self.root)
        controls_frame.pack(fill="x", padx=10, pady=(0, 10))

        amount_label = Label(controls_frame, text="Amount in BRL:")
        amount_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

        amount_entry = Entry(controls_frame)
        amount_entry.grid(row=0, column=1, padx=(0, 10), sticky="w" + "e")

        self.crypto_combobox = ttk.Combobox(controls_frame, state="readonly")
        self.crypto_combobox.grid(row=0, column=2, padx=5, pady=5, sticky="w" + "e")
        capitalized_cryptos = []

        for crypto in self.coin_manager.get_available_coins():
            capitalized_crypto = crypto.capitalize()
            tree.insert("", "end", values=(capitalized_crypto, 0, 0, 0))
            capitalized_cryptos.append(capitalized_crypto)

        self.crypto_combobox['values'] = capitalized_cryptos

        if capitalized_cryptos:
            self.crypto_combobox.current(0)

        buy_button = ttk.Button(controls_frame, text="Buy", command=self.buy_selected_crypto)
        buy_button.grid(row=0, column=3, padx=5, pady=5, sticky="w" + "e")

        sell_button = ttk.Button(controls_frame, text="Sell", command=self.sell_selected_crypto)
        sell_button.grid(row=0, column=4, padx=5, pady=5, sticky="w" + "e")

        return tree, controls_frame, amount_entry

    def reset_data(self):
        self.balance_manager.reset_balance()
        self.purchase_manager.reset_purchases()
        self.update_gui()

    def update_gui(self):
        self.balance_panel.update()
        self.table.update()
        
    def buy_selected_crypto(self):
        selected_crypto = self.crypto_combobox.get().lower()
        amount = float(self.amount_entry.get())
        self.purchase_manager.buy_crypto(selected_crypto, amount)
        self.update_gui()

    def sell_selected_crypto(self):
        selected_crypto = self.crypto_combobox.get().lower()
        amount = float(self.amount_entry.get())
        self.purchase_manager.sell_crypto(selected_crypto, amount)
        self.update_gui()
