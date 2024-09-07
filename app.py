from coin_manager import CoinManager
from dependencies import configure_injections
from gui import GUI
from utils import Utils
import inject

class App:
    @inject.autoparams()
    def __init__(self, gui: GUI):
        self.gui = gui
        self.utils = Utils()

    def main(self):
        self.gui.root.protocol("WM_DELETE_WINDOW", self.utils.on_closing)
        self.utils.fetch_crypto_prices()
        self.gui.root.mainloop()

if __name__ == "__main__":
    inject.configure(configure_injections)
    app = App()
    app.main()
