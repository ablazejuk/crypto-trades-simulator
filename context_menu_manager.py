from tkinter import Menu
from singleton_metaclass import SingletonMeta

class ContextMenuManager(metaclass=SingletonMeta):
    def setup_context_menu(self, root, tree):
        self.root = root
        self.tree = tree
        self.context_menu = Menu(self.tree, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self.copy_to_clipboard)

        self.tree.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        row_id = self.tree.identify_row(event.y)
        column_id = self.tree.identify_column(event.x)

        if row_id and column_id:
            self.tree.selection_set(row_id)
            self.tree.focus(row_id)
            self.selected_row = row_id
            self.selected_column = column_id
            self.context_menu.post(event.x_root, event.y_root)

    def copy_to_clipboard(self):
        value = self.tree.item(self.selected_row, 'values')[int(self.selected_column[1]) - 1]
        
        self.root.clipboard_clear()
        self.root.clipboard_append(value)
        self.root.update()
