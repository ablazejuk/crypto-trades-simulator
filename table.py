from tkinter import Frame, Tk, ttk
from coin_manager import CoinManager
import inject
from purchase_manager import PurchaseManager

class Table:
    @inject.autoparams()
    def __init__(self, coin_manager: CoinManager, purchase_manager: PurchaseManager):
        self.coin_manager = coin_manager
        self.purchase_manager = purchase_manager

    def create(self, root: Tk) -> ttk.Treeview:
        table_frame = Frame(root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        columns = ("Cryptocurrency", "Price (BRL)", "Quantity Bought", "Value in BRL")
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="e")

        self.tree.column("Cryptocurrency", anchor="w", stretch=True)
        self.tree.pack(side="left", fill="both", expand=True)

        return self.tree

    def update(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        for crypto, info in self.coin_manager.get_latest_prices().items():
            price = info['brl']
            quantity = round(self.purchase_manager.get_purchases().get(crypto, 0.0), 8)
            value_in_brl = round(quantity * price, 2)
            self.tree.insert("", "end", values=(crypto.capitalize(), f"{price:.2f}", f"{quantity:.8f}", f"{value_in_brl:.2f}"))
