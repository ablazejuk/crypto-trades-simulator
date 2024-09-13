from tkinter import Frame, Label, Entry, Tk, ttk, Button
from coin_manager import CoinManager
from context_menu_manager import ContextMenuManager
from data_manager import DataManager
import inject
from balance_manager import BalanceManager
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
        context_menu_manager: ContextMenuManager
    ):
        self.balance_manager = balance_manager
        self.purchase_manager = purchase_manager
        self.coin_manager = coin_manager
        self.data_manager = data_manager
        self.root = Tk()

        self.tree, self.balance_label, self.controls_frame, self.amount_entry = self.create_main_window()

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
        balance_frame = Frame(self.root)
        balance_frame.pack(fill="x", padx=10, pady=(10, 0))

        balance_label = Label(balance_frame, text=f"Balance: {self.balance_manager.get_balance():.2f} BRL")
        balance_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

        reset_button = Button(balance_frame, text="Reset", command=self.reset_data)
        reset_button.grid(row=0, column=1, sticky="e")

        table_frame = Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        CRYPTOCURRENCY = "Cryptocurrency"
        PRICE_BRL = "Price (BRL)"
        QUANTITY_BOUGHT = "Quantity Bought"
        VALUE_BRL = "Value in BRL"

        columns = (CRYPTOCURRENCY, PRICE_BRL, QUANTITY_BOUGHT, VALUE_BRL)
        tree = ttk.Treeview(table_frame, columns=columns, show='headings')

        tree.heading(CRYPTOCURRENCY, text=CRYPTOCURRENCY)
        tree.heading(PRICE_BRL, text=PRICE_BRL)
        tree.heading(QUANTITY_BOUGHT, text=QUANTITY_BOUGHT)
        tree.heading(VALUE_BRL, text=VALUE_BRL)

        tree.column(CRYPTOCURRENCY, anchor="w", stretch=True)
        tree.column(PRICE_BRL, anchor="e", stretch=True)
        tree.column(QUANTITY_BOUGHT, anchor="e", stretch=True)
        tree.column(VALUE_BRL, anchor="e", stretch=True)

        tree.pack(side="left", fill="both", expand=True)

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

        return tree, balance_label, controls_frame, amount_entry

    def reset_data(self):
        self.balance_manager.reset_balance()
        self.purchase_manager.reset_purchases()
        self.update_gui()

    def update_gui(self):
        self.balance_label.config(text=f"Balance: {self.balance_manager.get_balance():.2f} BRL")

        for item in self.tree.get_children():
            self.tree.delete(item)

        for crypto, info in self.coin_manager.get_latest_prices().items():
            price = info['brl']
            quantity = round(self.purchase_manager.get_purchases().get(crypto, 0.0), 8)
            value_in_brl = round(quantity * price, 2)
            self.tree.insert("", "end", values=(crypto.capitalize(), f"{price:.2f}", f"{quantity:.8f}", f"{value_in_brl:.2f}"))
        
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
