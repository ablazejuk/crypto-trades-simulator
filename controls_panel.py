from tkinter import Entry, Frame, Label, ttk
from coin_manager import CoinManager
import inject
from purchase_manager import PurchaseManager
from singleton_metaclass import SingletonMeta

class ControlsPanel(metaclass=SingletonMeta):
    @inject.autoparams()
    def __init__(self, purchase_manager: PurchaseManager, coin_manager: CoinManager):
        self.purchase_manager = purchase_manager
        self.coin_manager = coin_manager

    def create(self, root, update_callback):
        self.update_callback = update_callback

        controls_frame = Frame(root)
        controls_frame.pack(fill="x", padx=10, pady=(0, 10))

        Label(controls_frame, text="Amount in BRL:").grid(row=0, column=0, padx=(0, 10), sticky="w")

        self.amount_entry = Entry(controls_frame)
        self.amount_entry.grid(row=0, column=1, padx=(0, 10), sticky="w" + "e")

        self.crypto_combobox = ttk.Combobox(controls_frame, state="readonly")
        self.crypto_combobox.grid(row=0, column=2, padx=5, pady=5, sticky="w" + "e")

        self.populate_combobox()

        buy_button = ttk.Button(controls_frame, text="Buy", command=self.buy_selected_crypto)
        buy_button.grid(row=0, column=3, padx=5, pady=5, sticky="w" + "e")

        sell_button = ttk.Button(controls_frame, text="Sell", command=self.sell_selected_crypto)
        sell_button.grid(row=0, column=4, padx=5, pady=5, sticky="w" + "e")

    def populate_combobox(self):
        capitalized_cryptos = [crypto.capitalize() for crypto in self.coin_manager.get_available_coins()]
        self.crypto_combobox['values'] = capitalized_cryptos
        if capitalized_cryptos:
            self.crypto_combobox.current(0)

    def buy_selected_crypto(self):
        selected_crypto = self.crypto_combobox.get().lower()
        amount = float(self.amount_entry.get())
        self.purchase_manager.buy_crypto(selected_crypto, amount)
        self.update_callback()

    def sell_selected_crypto(self):
        selected_crypto = self.crypto_combobox.get().lower()
        amount = float(self.amount_entry.get())
        self.purchase_manager.sell_crypto(selected_crypto, amount)
        self.update_callback()