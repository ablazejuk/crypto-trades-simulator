from tkinter import Tk
from utils import load_data, fetch_crypto_prices, update_prices, on_closing
from gui import create_main_window

def main():
    # Initialize the main window
    root = Tk()

    # Load data
    balance, purchases = load_data()

    # Initialize latest_prices as an empty dictionary
    latest_prices = {}

    # Set up the main window and GUI components
    tree, balance_label, controls_frame, amount_entry = create_main_window(root, balance, purchases)

    # Set up the window close protocol
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, balance, purchases))

    # Fetch initial prices and start updating prices
    fetch_crypto_prices(root, tree, purchases, latest_prices, balance, balance_label, controls_frame, amount_entry)
    update_prices(tree, purchases, latest_prices, balance, balance_label, controls_frame, amount_entry)

    # Set the window size and start the main event loop
    root.geometry("900x600")
    root.mainloop()

if __name__ == "__main__":
    main()
