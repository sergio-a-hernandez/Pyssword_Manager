import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import pyperclip

class PasswordManagerGUI:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        root.title("Password Manager - Pyssword_Manager")

        tk.Label(root, text="ID:").grid(row=0, column=0)
        tk.Label(root, text="Site:").grid(row=1, column=0)
        tk.Label(root, text="Username:").grid(row=2, column=0)
        tk.Label(root, text="Password:").grid(row=3, column=0)

        self.id_entry = tk.Entry(root, width=30, state="readonly")
        self.site_entry = tk.Entry(root, width=30)
        self.user_entry = tk.Entry(root, width=30)
        self.pass_entry = tk.Entry(root, width=30)

        self.id_entry.grid(row=0, column=1)
        self.site_entry.grid(row=1, column=1)
        self.user_entry.grid(row=2, column=1)
        self.pass_entry.grid(row=3, column=1)

        button_frame = tk.Frame(root)
        button_frame.grid(row=5, column=0, columnspan=5, pady=(10, 5))

        tk.Button(button_frame, text="New entry", command=self.new_entry).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Generate secure password", command=self.generate).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Save entry", command=self.save_password).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Show all passwords", command=self.show_passwords).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="Hide passwords", command=self.populate_tree).grid(row=0, column=4, padx=5)

        self.tree = ttk.Treeview(root, columns=("ID", "Site", "Username", "Password"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Site", text="Site")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Password", text="Password")
        self.tree.grid(row=6, column=0, columnspan=5, pady=10, sticky="nsew")

        root.grid_rowconfigure(6, weight=1)
        root.grid_columnconfigure(1, weight=1)

        self.tree.bind("<Button-1>", self.on_tree_click)
        self.tree.bind("<Double-1>", self.on_tree_double_click)

        self.populate_tree()

    def clear_entries(self):
        self.id_entry.config(state="normal")
        self.id_entry.delete(0, tk.END)
        self.id_entry.config(state="readonly")
        self.site_entry.delete(0, tk.END)
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)

    def new_entry(self):
        self.clear_entries()
        self.id_entry.config(state="normal")
        self.id_entry.insert(0, "New")
        self.id_entry.config(state="readonly")
        self.site_entry.focus_set()

    def save_password(self):
        ide = self.id_entry.get()
        site = self.site_entry.get()
        user = self.user_entry.get()
        pwd = self.pass_entry.get()
        if not site or not user or not pwd:
            messagebox.showwarning("Incomplete fields", "Please fill in all fields.")
            return
        self.controller.save_password(ide, site, user, pwd)
        self.populate_tree()
        messagebox.showinfo("Saved", "Password saved successfully.")

    def generate(self):
        pwd = self.controller.generate_password()
        self.pass_entry.delete(0, tk.END)
        self.pass_entry.insert(0, pwd)
        pyperclip.copy(pwd)
        messagebox.showinfo("Generated", "Password copied to clipboard.")

    def show_passwords(self):
        temp_key = simpledialog.askstring("Master Password Required", "Enter your master password to show all saved passwords:", show="*")
        if not temp_key:
            return
        self.controller.show_passwords(temp_key, self.tree)
        self.new_entry()

    def populate_tree(self):
        self.controller.populate_tree(self.tree)
        self.new_entry()

    def on_tree_click(self, event):
        item = self.tree.selection()
        if not item:
            return
        item = item[0]
        ide, site, username, password = self.tree.item(item, "values")
        self.clear_entries()
        self.id_entry.config(state="normal")
        self.id_entry.insert(0, ide)
        self.id_entry.config(state="readonly")
        self.site_entry.insert(0, site)
        self.user_entry.insert(0, username)
        self.pass_entry.insert(0, "********")

    def on_tree_double_click(self, event):
        item = self.tree.selection()
        if not item:
            return
        item = item[0]
        ide, site, username, _ = self.tree.item(item, "values")
        self.controller.copy_password(ide, site, username)
        self.on_tree_click()
