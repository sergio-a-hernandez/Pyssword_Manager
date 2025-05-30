import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import pyperclip

from crypto import get_fernet
import database
import password_generator

# Save a password to the encrypted database
def save_password():
    site = site_entry.get()
    user = user_entry.get()
    pwd = pass_entry.get()
    if not site or not user or not pwd:
        messagebox.showwarning("Incomplete fields", "Please fill in all fields.")
        return
    database.insert_password(site, user, pwd, fernet)
    site_entry.delete(0, tk.END)
    user_entry.delete(0, tk.END)
    pass_entry.delete(0, tk.END)
    messagebox.showinfo("Saved", "Password saved successfully.")

# Generate a secure password, insert into field and copy to clipboard
def generate():
    pwd = password_generator.generate_password()
    pass_entry.delete(0, tk.END)
    pass_entry.insert(0, pwd)
    pyperclip.copy(pwd)
    messagebox.showinfo("Generated", "Password copied to clipboard.")

# Ask for master key and show all passwords if valid
def show_passwords():
    temp_key = simpledialog.askstring("Master Password Required", "Enter your master password to show all saved passwords:", show="*")
    if not temp_key:
        return

    try:
        temp_fernet = get_fernet(temp_key)
        records = database.get_raw_passwords()

        # Clear table
        for item in tree.get_children():
            tree.delete(item)

        # Decrypt and display each password
        for site, enc_user, enc_pass in records:
            try:
                username = temp_fernet.decrypt(enc_user).decode()
                password = temp_fernet.decrypt(enc_pass).decode()
                tree.insert("", "end", values=(site, username, password))
            except Exception:
                continue

    except Exception:
        messagebox.showerror("Error", "Incorrect master password or decryption error.")

# Load existing records with usernames and masked passwords
def populate_tree():
    for item in tree.get_children():
        tree.delete(item)

    for site, enc_user, _ in database.get_raw_passwords():
        try:
            username = fernet.decrypt(enc_user).decode()
            password = "********"
            tree.insert("", "end", values=(site, username, password))
        except Exception:
            continue

# Handle double-click event to show and copy password to clipboard
def on_tree_double_click(event):
    item = tree.selection()[0]
    site, username = tree.item(item, "values")

    for s, enc_user, enc_pass in database.get_raw_passwords():
        try:
            u = fernet.decrypt(enc_user).decode()
            if s == site and u == username:
                password = fernet.decrypt(enc_pass).decode()
                pyperclip.copy(password)
                messagebox.showinfo("Copied", f"Site: {site}\nUsername: {username}\nPassword copied to clipboard.")
                break
        except Exception:
            continue

# Initialize the UI
def init_ui():
    global site_entry, user_entry, pass_entry, tree
    root = tk.Tk()
    root.title("Password Manager - Pyssword_Manager")

    tk.Label(root, text="Site:").grid(row=0, column=0)
    tk.Label(root, text="Username:").grid(row=1, column=0)
    tk.Label(root, text="Password:").grid(row=2, column=0)

    site_entry = tk.Entry(root, width=40)
    user_entry = tk.Entry(root, width=40)
    pass_entry = tk.Entry(root, width=40)

    site_entry.grid(row=0, column=1)
    user_entry.grid(row=1, column=1)
    pass_entry.grid(row=2, column=1)

    tk.Button(root, text="Save", command=save_password).grid(row=3, column=0)
    tk.Button(root, text="Generate", command=generate).grid(row=3, column=1)
    tk.Button(root, text="Show All", command=show_passwords).grid(row=4, column=0, columnspan=2)

    # Table to show saved entries
    tree = ttk.Treeview(root, columns=("Site", "Username", "Password"), show="headings")
    tree.heading("Site", text="Site")
    tree.heading("Username", text="Username")
    tree.heading("Password", text="Password")
    tree.grid(row=5, column=0, columnspan=3, pady=10, sticky="nsew")

    # Make the table resizable
    root.grid_rowconfigure(5, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Double-click event to copy password
    tree.bind("<Double-1>", on_tree_double_click)

    # Populate the table on startup
    populate_tree()

    root.mainloop()

# Entry point
if __name__ == "__main__":
    master_key = simpledialog.askstring("Master Key", "Enter your master key:", show="*")
    if not master_key:
        messagebox.showerror("Error", "Master key is required.")
        exit(1)

    if len(master_key) < 12:
        messagebox.showerror("Weak Key", "Master key must be at least 12 characters long.")
        exit(1)

    fernet = get_fernet(master_key)
    database.create_db()
    init_ui()
