from tkinter import Tk
from gui import CryptoGUI
from utils import CryptoUtils

def main():
    # Initialize the main window
    root = Tk()

    # Initialize GUI and Utils classes
    gui = CryptoGUI(root, balance=100.0, purchases={})
    utils = CryptoUtils(gui)

    # Load data
    utils.load_data()

    # Set up the window close protocol
    root.protocol("WM_DELETE_WINDOW", utils.on_closing)

    # Fetch initial prices and start updating prices
    utils.fetch_crypto_prices()

    # Set the window size and start the main event loop
    root.geometry("900x600")
    root.mainloop()

if __name__ == "__main__":
    main()
