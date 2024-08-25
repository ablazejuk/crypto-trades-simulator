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
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        print("API Response:", data)  # Log the API response to the console
        return data
    except requests.RequestException as e:
        print("Request Error:", e)  # Log any request errors to the console
        return str(e)

def update_prices():
    prices = fetch_crypto_prices()
    if isinstance(prices, dict):
        for item in tree.get_children():
            tree.delete(item)  # Clear the existing table rows
        for crypto, info in prices.items():
            price = info['brl']
            quantity = round(purchases.get(crypto, 0.0), 8)  # Round quantity to 8 decimal places
            value_in_brl = round(quantity * price, 2)  # Calculate value in BRL and round to 2 decimal places
            tree.insert("", tk.END, values=(crypto.capitalize(), price, quantity, value_in_brl))
        readjust_columns()
    else:
        for item in tree.get_children():
            tree.delete(item)
        tree.insert("", tk.END, values=("Error", prices))

    # Update the balance label
    balance_label.config(text=f"Balance: {balance:.2f} BRL")

    # Schedule the next update after 60 seconds (60000 milliseconds)
    root.after(60000, update_prices)

def buy_crypto(crypto, price):
    global balance
    try:
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

def readjust_columns():
    for col in columns:
        tree.column(col, anchor=tk.CENTER, stretch=True)  # Align the text in the center
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create the main window
root = tk.Tk()
load_data()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.title("Crypto Trades Simulator")

# Create a frame for the button and add the button
button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X, padx=10, pady=10)

fetch_button = tk.Button(button_frame, text="Fetch Prices", command=update_prices)
fetch_button.pack(pady=10)

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

# Create a frame for the entry and buttons
controls_frame = tk.Frame(root)
controls_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

# Create an entry for the amount to buy
amount_label = tk.Label(controls_frame, text="Amount in BRL:")
amount_label.pack(side=tk.LEFT)

amount_entry = tk.Entry(controls_frame)
amount_entry.pack(side=tk.LEFT, padx=(0, 10))

# Function to add buy buttons
def add_buy_buttons():
    # Remove previous buy buttons
    for widget in controls_frame.winfo_children():
        if isinstance(widget, tk.Button):
            widget.destroy()

    for item in tree.get_children():
        values = tree.item(item, 'values')
        crypto = values[0].lower()  # Use cryptocurrency name
        price = float(values[1])  # Convert price to float
        buy_button = tk.Button(controls_frame, text=f"Buy {crypto.capitalize()}", command=lambda c=crypto, p=price: buy_crypto(c, p))
        buy_button.pack(side=tk.LEFT, padx=5, pady=5)

# Bind the update_prices call to initial run and button creation
update_prices()
add_buy_buttons()

# Set a minimum size for the window to ensure everything fits
root.geometry("800x400")  # Adjust as needed

# Run the application
root.mainloop()