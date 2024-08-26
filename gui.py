import tkinter as tk
from tkinter import ttk
import requests
import json
import os

data_file = "crypto_data.json"

# Define the endpoint and parameters
url = 'https://api.coingecko.com/api/v3/simple/price'
params = {
    'ids': 'bitcoin,ethereum,solana,sundog',
    'vs_currencies': 'brl'
}

# Initial balance and purchase tracking
balance = 100.0
purchases = {
    'bitcoin': 0.0,
    'ethereum': 0.0,
    'solana': 0.0,
    'sundog': 0.0
}

# Store the latest prices globally
latest_prices = {}

def save_data():
    data = {
        "balance": balance,
        "purchases": purchases
    }
    with open(data_file, "w") as f:
        json.dump(data, f)
    print("Data saved.")

def load_data():
    global balance, purchases
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            data = json.load(f)
            balance = data.get("balance", 100.0)  # Default to 100 BRL if not found
            purchases = data.get("purchases", {})
            print("Data loaded.")
    else:
        balance = 100.0
        purchases = {}

def on_closing():
    save_data()
    root.destroy()

def fetch_crypto_prices():
    global latest_prices
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        print("API Response:", data)  # Log the API response to the console
        latest_prices = data  # Update global latest prices
    except requests.RequestException as e:
        print("Request Error:", e)  # Log any request errors to the console
    
    # Schedule the next update after 60 seconds (60000 milliseconds)
    root.after(60000, fetch_crypto_prices)

def update_prices():
    for item in tree.get_children():
        tree.delete(item)  # Clear the existing table rows
    for crypto, info in latest_prices.items():
        price = info['brl']
        quantity = round(purchases.get(crypto, 0.0), 8)  # Round quantity to 8 decimal places
        value_in_brl = round(quantity * price, 2)  # Calculate value in BRL and round to 2 decimal places
        tree.insert("", tk.END, values=(crypto.capitalize(), price, quantity, value_in_brl))
    readjust_columns()

    # Update the balance label
    balance_label.config(text=f"Balance: {balance:.2f} BRL")

    # Update buttons after prices update
    add_buy_sell_buttons()

def buy_crypto(crypto):
    global balance
    try:
        price = latest_prices[crypto]['brl']
        amount_str = amount_entry.get().strip()  # Get and strip whitespace from the amount entry
        if not amount_str:
            raise ValueError("Amount cannot be empty.")
        amount_brl = float(amount_str)  # Convert to float
        if amount_brl <= 0:
            raise ValueError("Amount must be positive.")
        quantity = amount_brl / price  # Calculate the quantity of cryptocurrency
        if balance >= amount_brl:
            balance -= amount_brl  # Subtract the entered amount directly from the balance
            purchases[crypto] = round(purchases.get(crypto, 0.0) + quantity, 8)  # Update and round the quantity
            update_prices()  # Update the table with new quantities
            print(f"Bought {quantity:.8f} of {crypto} for {amount_brl:.2f} BRL.")
        else:
            print("Insufficient balance.")
    except ValueError as e:
        print(f"Error: {e}")

def sell_crypto(crypto):
    global balance
    try:
        price = latest_prices[crypto]['brl']
        amount_str = amount_entry.get().strip()  # Get and strip whitespace from the amount entry
        if not amount_str:
            raise ValueError("Amount cannot be empty.")
        amount_brl = float(amount_str)  # Convert to float
        if amount_brl <= 0:
            raise ValueError("Amount must be positive.")
        quantity_to_sell = amount_brl / price  # Calculate the quantity of cryptocurrency to sell
        if purchases[crypto] >= quantity_to_sell:
            purchases[crypto] = round(purchases.get(crypto, 0.0) - quantity_to_sell, 8)  # Update and round the quantity
            balance += amount_brl  # Add the amount in BRL back to the balance
            update_prices()  # Update the table with new quantities
            print(f"Sold {quantity_to_sell:.8f} of {crypto} for {amount_brl:.2f} BRL.")
        else:
            print("Insufficient cryptocurrency quantity to sell.")
    except ValueError as e:
        print(f"Error: {e}")

def readjust_columns():
    for col in columns:
        tree.column(col, anchor=tk.CENTER, stretch=True)  # Align the text in the center
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

def add_buy_sell_buttons():
    # Remove previous buttons
    for widget in controls_frame.winfo_children():
        if isinstance(widget, tk.Button):
            widget.grid_forget()  # Use grid_forget() instead of destroy() for layout adjustments

    # Create a button grid dynamically
    row = 1  # Start below the input field
    for item in tree.get_children():
        values = tree.item(item, 'values')
        crypto = values[0].lower()  # Use cryptocurrency name
        
        buy_button = tk.Button(controls_frame, text=f"Buy {crypto.capitalize()}", command=lambda c=crypto: buy_crypto(c))
        buy_button.grid(row=row, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
        
        sell_button = tk.Button(controls_frame, text=f"Sell {crypto.capitalize()}", command=lambda c=crypto: sell_crypto(c))
        sell_button.grid(row=row, column=1, padx=5, pady=5, sticky=tk.W+tk.E)

        row += 1

def copy_value_to_clipboard(event):
    selected_item = tree.selection()[0]  # Get the selected item
    values = tree.item(selected_item, 'values')
    value_in_brl = values[3]  # Get the "Value in BRL" column value
    root.clipboard_clear()
    root.clipboard_append(value_in_brl)
    print(f"Copied to clipboard: {value_in_brl}")

# Create the main window
root = tk.Tk()
load_data()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.title("Crypto Trades Simulator")

# Create a frame for the balance label
balance_frame = tk.Frame(root)
balance_frame.pack(fill=tk.X, padx=10, pady=(10, 0))

# Create a label to display the balance
balance_label = tk.Label(balance_frame, text=f"Balance: {balance:.2f} BRL")
balance_label.pack()

# Create a frame for the table and amount entry
table_frame = tk.Frame(root)
table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

# Create a Treeview widget for the table
columns = ("Cryptocurrency", "Price (BRL)", "Quantity Bought", "Value in BRL")
tree = ttk.Treeview(table_frame, columns=columns, show='headings')
tree.heading("Cryptocurrency", text="Cryptocurrency")
tree.heading("Price (BRL)", text="Price (BRL)")
tree.heading("Quantity Bought", text="Quantity Bought")
tree.heading("Value in BRL", text="Value in BRL")
tree.column("Cryptocurrency", anchor=tk.W, stretch=True)
tree.column("Price (BRL)", anchor=tk.E, stretch=True)
tree.column("Quantity Bought", anchor=tk.E, stretch=True)
tree.column("Value in BRL", anchor=tk.E, stretch=True)

# Insert initial rows with zero values
for crypto in purchases.keys():
    tree.insert("", tk.END, values=(crypto.capitalize(), 0, 0, 0))

tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Bind double-click event to copy value to clipboard
tree.bind("<Double-1>", copy_value_to_clipboard)

# Create a frame for the input and buttons
controls_frame = tk.Frame(root)
controls_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

# Create an entry for the amount to buy/sell
amount_label = tk.Label(controls_frame, text="Amount in BRL:")
amount_label.grid(row=0, column=0, padx=(0, 10), sticky=tk.W)

amount_entry = tk.Entry(controls_frame)
amount_entry.grid(row=0, column=1, padx=(0, 10), sticky=tk.W+tk.E)

# Add buy and sell buttons
add_buy_sell_buttons()

# Fetch initial prices and start updating prices
fetch_crypto_prices()  # Fetch prices initially
update_prices()  # Start updating prices every minute

# Set a minimum size for the window to ensure everything fits
root.geometry("900x600")  # Increased size to fit buttons

# Run the application
root.mainloop()
