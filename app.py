from coin_manager import CoinManager
from dependencies import configure_injections
from tkinter import Tk
from gui import GUI
from purchase_manager import PurchaseManager
from utils import Utils
import inject
from balance_manager import BalanceManager

class App:
    def __init__(self):
        self.root = Tk()
        self.gui = GUI(inject.instance(BalanceManager), inject.instance(PurchaseManager), inject.instance(CoinManager), self.root)
        self.utils = Utils(inject.instance(CoinManager), self.gui)

    def main(self):
        self.root.title("Crypto Trades Simulator")
        self.root.protocol("WM_DELETE_WINDOW", self.utils.on_closing)
        self.utils.fetch_crypto_prices()
        self.root.geometry("900x600")
        self.root.mainloop()

if __name__ == "__main__":
    inject.configure(configure_injections)
    app = App()
    app.main()
