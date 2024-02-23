import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import pyperclip

class ClipboardHistoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clipboard History")
        
        self.clipboard_history = []
        self.max_history_items = 10  # Maximum number of items to keep in history

        self.create_widgets()
        self.update_clipboard_periodically()

    def create_widgets(self):
        self.treeview = ttk.Treeview(self.root, columns=("Content",), selectmode="browse")
        self.treeview.heading("#0", text="Index")
        self.treeview.heading("Content", text="Content")
        self.treeview.column("#0", width=50)
        self.treeview.column("Content", width=300)
        self.treeview.pack(expand=True, fill="both")

        self.refresh_button = ttk.Button(self.root, text="Refresh", command=self.refresh_history)
        self.refresh_button.pack()

        self.paste_button = ttk.Button(self.root, text="Paste", command=self.paste_selected)
        self.paste_button.pack()

        self.refresh_history()

    def refresh_history(self):
        # Clear existing items in treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        # Display clipboard history in treeview
        for i, item in enumerate(self.clipboard_history):
            self.treeview.insert("", "end", text=str(i+1), values=(item,))

    def paste_selected(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No item selected.")
            return
        
        index = int(self.treeview.item(selected_item)["text"]) - 1
        if index < 0 or index >= len(self.clipboard_history):
            messagebox.showwarning("Warning", "Invalid selection.")
            return
        
        content = self.clipboard_history[index]
        pyperclip.copy(content)
        # messagebox.showinfo("Info", f"Content '{content}' copied to clipboard.")

    def update_clipboard_periodically(self):
        self.update_clipboard()
        self.root.after(1000, self.update_clipboard_periodically)  # Update clipboard every 2 seconds

    def update_clipboard(self):
        clipboard_content = pyperclip.paste()
        if clipboard_content:
            if not self.clipboard_history or clipboard_content != self.clipboard_history[0]:
                self.clipboard_history.insert(0, clipboard_content)
                self.clipboard_history = self.clipboard_history[:self.max_history_items]
                self.refresh_history()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardHistoryApp(root)
    root.mainloop()