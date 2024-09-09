from gui import GUI
import inject
import json

data_file = "crypto_data.json"

class Utils:
    @inject.autoparams()
    def __init__(self, gui: GUI):
        self.gui = gui

    def save_data(self):
        data = {"balance": self.gui.balance_manager.get_balance(), "purchases": self.gui.purchase_manager.get_purchases()}
        with open(data_file, "w") as f:
            json.dump(data, f)
        print("Data saved.")

    def on_closing(self):
        self.save_data()
