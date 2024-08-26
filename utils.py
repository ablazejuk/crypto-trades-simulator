import tkinter as tk
import requests
import json
import os

data_file = "crypto_data.json"
url = 'https://api.coingecko.com/api/v3/simple/price'
params = {'ids': 'bitcoin,ethereum,solana,sundog', 'vs_currencies': 'brl'}

def save_data(balance, purchases):
    data = {"balance": balance, "purchases": purchases}
    with open(data_file, "w") as f:
        json.dump(data, f)
    print("Data saved.")

def load_data():
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            data = json.load(f)
            balance = data.get("balance", 100.0)
            purchases = data.get("purchases", {})
            print("Data loaded.")
            return balance, purchases
    else:
        return 100.0, {'bitcoin': 0.0, 'ethereum': 0.0, 'solana': 0.0, 'sundog': 0.0}

def fetch_crypto_prices(root, tree, purchases, latest_prices, balance, balance_label, controls_frame, amount_entry):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        print("API Response:", data)  # Log the API response to the console
        latest_prices.update(data)  # Update the dictionary in-place
    except requests.RequestException as e:
        print("Request Error:", e)  # Log any request errors to the console

    update_prices(tree, purchases, latest_prices, balance, balance_label, controls_frame, amount_entry)
    
    # Schedule the next update after 60 seconds (60000 milliseconds)
    root.after(60000, fetch_crypto_prices, root, tree, purchases, latest_prices, balance, balance_label, controls_frame, amount_entry)

def add_buy_sell_buttons(controls_frame, tree, purchases, balance, latest_prices, amount_entry):
    # Remove previous buttons
    for widget in controls_frame.winfo_children():
        if isinstance(widget, tk.Button):
            widget.grid_forget()  # Use grid_forget() instead of destroy() for layout adjustments

    # Create a button grid dynamically
    row = 1  # Start below the input field
    for item in tree.get_children():
        values = tree.item(item, 'values')
        crypto = values[0].lower()  # Use cryptocurrency name

        buy_button = tk.Button(controls_frame, text=f"Buy {crypto.capitalize()}", command=lambda c=crypto: buy_crypto(c, purchases, balance, latest_prices, amount_entry))
        buy_button.grid(row=row, column=0, padx=5, pady=5, sticky=tk.W+tk.E)

        sell_button = tk.Button(controls_frame, text=f"Sell {crypto.capitalize()}", command=lambda c=crypto: sell_crypto(c, purchases, balance, latest_prices, amount_entry))
        sell_button.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W+tk.E)

        row += 1

def on_closing(root, balance, purchases):
    save_data(balance, purchases)
    root.destroy()


def update_prices(tree, purchases, latest_prices, balance, balance_label, controls_frame, amount_entry):
    for item in tree.get_children():
        tree.delete(item)
    for crypto, info in latest_prices.items():
        price = info['brl']
        quantity = round(purchases.get(crypto, 0.0), 8)
        value_in_brl = round(quantity * price, 2)
        tree.insert("", tk.END, values=(crypto.capitalize(), price, quantity, value_in_brl))
    readjust_columns(tree)

    balance_label.config(text=f"Balance: {balance:.2f} BRL")
    add_buy_sell_buttons(controls_frame, tree, purchases, balance, latest_prices, amount_entry)

def readjust_columns(tree):
    columns = ["Cryptocurrency", "Price (BRL)", "Quantity Bought", "Value in BRL"]
    for col in columns:
        tree.column(col, anchor=tk.CENTER, stretch=True)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
