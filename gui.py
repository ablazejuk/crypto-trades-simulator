from tkinter import Frame, Label, Entry
from tkinter import ttk

def create_main_window(root, balance, purchases):
    # Create a frame for the balance label
    balance_frame = Frame(root)
    balance_frame.pack(fill="x", padx=10, pady=(10, 0))

    # Create a label to display the balance
    balance_label = Label(balance_frame, text=f"Balance: {balance:.2f} BRL")
    balance_label.pack()

    # Create a frame for the table and amount entry
    table_frame = Frame(root)
    table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # Create a Treeview widget for the table
    columns = ("Cryptocurrency", "Price (BRL)", "Quantity Bought", "Value in BRL")
    tree = ttk.Treeview(table_frame, columns=columns, show='headings')
    tree.heading("Cryptocurrency", text="Cryptocurrency")
    tree.heading("Price (BRL)", text="Price (BRL)")
    tree.heading("Quantity Bought", text="Quantity Bought")
    tree.heading("Value in BRL", text="Value in BRL")

    tree.column("Cryptocurrency", anchor="w", stretch=True)
    tree.column("Price (BRL)", anchor="e", stretch=True)
    tree.column("Quantity Bought", anchor="e", stretch=True)
    tree.column("Value in BRL", anchor="e", stretch=True)

    # Insert initial rows with zero values
    for crypto in purchases.keys():
        tree.insert("", "end", values=(crypto.capitalize(), 0, 0, 0))

    tree.pack(side="left", fill="both", expand=True)

    # Create a frame for the input and buttons
    controls_frame = Frame(root)
    controls_frame.pack(fill="x", padx=10, pady=(0, 10))

    # Create an entry for the amount to buy/sell
    amount_label = Label(controls_frame, text="Amount in BRL:")
    amount_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

    amount_entry = Entry(controls_frame)
    amount_entry.grid(row=0, column=1, padx=(0, 10), sticky="w"+"e")

    return tree, balance_label, controls_frame, amount_entry
