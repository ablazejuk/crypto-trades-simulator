from tkinter import Tk
from gui import GUI
from utils import Utils

def main():
    root = Tk()

    gui = GUI(root, balance=100.0, purchases={})
    utils = Utils(gui)

    utils.load_data()

    root.protocol("WM_DELETE_WINDOW", utils.on_closing)

    utils.fetch_crypto_prices()

    root.geometry("900x600")
    root.mainloop()

if __name__ == "__main__":
    main()
