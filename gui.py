from tkinter import Frame, Label, Entry, ttk, Menu

class CryptoGUI:
    def __init__(self, root, balance, purchases):
        self.root = root
        self.balance = balance
        self.purchases = purchases
        self.latest_prices = {}

        # Initialize GUI components
        self.tree, self.balance_label, self.controls_frame, self.amount_entry = self.create_main_window()

        # Create a context menu for right-click
        self.context_menu = Menu(self.tree, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self.copy_to_clipboard)

        # Bind right-click to the treeview
        self.tree.bind("<Button-3>", self.show_context_menu)

    def create_main_window(self):
        # Create a frame for the balance label
        balance_frame = Frame(self.root)
        balance_frame.pack(fill="x", padx=10, pady=(10, 0))

        # Create a label to display the balance
        balance_label = Label(balance_frame, text=f"Balance: {self.balance:.2f} BRL")
        balance_label.pack()

        # Create a frame for the table and amount entry
        table_frame = Frame(self.root)
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
        for crypto in self.purchases.keys():
            tree.insert("", "end", values=(crypto.capitalize(), 0, 0, 0))

        tree.pack(side="left", fill="both", expand=True)

        # Create a frame for the input and buttons
        controls_frame = Frame(self.root)
        controls_frame.pack(fill="x", padx=10, pady=(0, 10))

        # Create an entry for the amount to buy/sell
        amount_label = Label(controls_frame, text="Amount in BRL:")
        amount_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

        amount_entry = Entry(controls_frame)
        amount_entry.grid(row=0, column=1, padx=(0, 10), sticky="w"+"e")

        return tree, balance_label, controls_frame, amount_entry

    def update_gui(self):
        # Update the balance label
        self.balance_label.config(text=f"Balance: {self.balance:.2f} BRL")

        # Clear the table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Reinsert updated data into the table
        for crypto, info in self.latest_prices.items():
            price = info['brl']
            quantity = round(self.purchases.get(crypto, 0.0), 8)
            value_in_brl = round(quantity * price, 2)
            self.tree.insert("", "end", values=(crypto.capitalize(), price, quantity, value_in_brl))

        # Re-add the buy and sell buttons with updated state
        self.add_buy_sell_buttons()

    def add_buy_sell_buttons(self):
        # Remove previous buttons
        for widget in self.controls_frame.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.grid_forget()

        # Create a button grid dynamically
        row = 1  # Start below the input field
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            crypto = values[0].lower()

            buy_button = ttk.Button(self.controls_frame, text=f"Buy {crypto.capitalize()}", command=lambda c=crypto: self.buy_crypto(c))
            buy_button.grid(row=row, column=0, padx=5, pady=5, sticky="w" + "e")

            sell_button = ttk.Button(self.controls_frame, text=f"Sell {crypto.capitalize()}", command=lambda c=crypto: self.sell_crypto(c))
            sell_button.grid(row=row, column=1, padx=5, pady=5, sticky="w" + "e")

            row += 1

    def buy_crypto(self, crypto):
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            print("Invalid amount entered.")
            return

        price = self.latest_prices[crypto]['brl']
        quantity = amount / price

        if self.balance >= amount:
            self.balance -= amount
            self.purchases[crypto] = self.purchases.get(crypto, 0) + quantity
            print(f"Bought {quantity:.8f} {crypto.capitalize()} for {amount:.2f} BRL.")
            self.update_gui()
        else:
            print("Insufficient balance.")

    def sell_crypto(self, crypto):
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            print("Invalid amount entered.")
            return

        price = self.latest_prices[crypto]['brl']
        quantity = amount / price

        if self.purchases.get(crypto, 0) >= quantity:
            self.purchases[crypto] -= quantity
            self.balance += amount
            print(f"Sold {quantity:.8f} {crypto.capitalize()} for {amount:.2f} BRL.")
            self.update_gui()
        else:
            print("Insufficient cryptocurrency to sell.")

    def show_context_menu(self, event):
        # Get the selected item
        row_id = self.tree.identify_row(event.y)
        column_id = self.tree.identify_column(event.x)

        if row_id and column_id:
            self.tree.selection_set(row_id)
            self.tree.focus(row_id)
            self.selected_row = row_id
            self.selected_column = column_id
            self.context_menu.post(event.x_root, event.y_root)

    def copy_to_clipboard(self):
        # Get the value of the selected cell
        value = self.tree.item(self.selected_row, 'values')[int(self.selected_column[1]) - 1]
        
        # Copy to clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(value)
        self.root.update()  # Keeps the clipboard content even after the app is closed
