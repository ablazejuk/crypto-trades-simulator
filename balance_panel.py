from tkinter import Button, Frame, Label
from balance_manager import BalanceManager
import inject
from singleton_metaclass import SingletonMeta

class BalancePanel(metaclass=SingletonMeta):
    @inject.autoparams()
    def __init__(self, balance_manager: BalanceManager):
        self.balance_manager = balance_manager
        
    def create(self, root, reset_callback):
        balance_frame = Frame(root)
        balance_frame.pack(fill="x", padx=10, pady=(10, 0))

        self.balance_label = Label(balance_frame, text=f"Balance: {self.balance_manager.get_balance():.2f} BRL")
        self.balance_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

        reset_button = Button(balance_frame, text="Reset", command=reset_callback)
        reset_button.grid(row=0, column=1, sticky="e")

    def update(self):
        self.balance_label.config(text=f"Balance: {self.balance_manager.get_balance():.2f} BRL")
