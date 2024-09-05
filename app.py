from tkinter import Tk
from gui import GUI
from utils import Utils
import dependencies
import inject
from balance_manager import BalanceManager

class App:
    def __init__(self):
        self.root = Tk()
        self.gui = GUI(inject.instance(BalanceManager), self.root, purchases={})
        self.utils = Utils(self.gui)

    def main(self):
        self.root.title("Crypto Trades Simulator")
        self.utils.load_data()
        self.root.protocol("WM_DELETE_WINDOW", self.utils.on_closing)
        self.utils.fetch_crypto_prices()
        self.root.geometry("900x600")
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.main()
