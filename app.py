from tkinter import messagebox
import database
import password_generator
from crypto import get_fernet
import pyperclip

class PasswordManagerApp:
    def __init__(self, master_key):
        if len(master_key) < 12:
            raise ValueError("Master key must be at least 12 characters long.")
        self.fernet = get_fernet(master_key)
        database.create_db()

    def save_password(self, ide, site, user, pwd):
        if ide.isdigit():
            database.update_password(ide, site, user, pwd, self.fernet)
        else:
            database.insert_password(site, user, pwd, self.fernet)

    def generate_password(self):
        return password_generator.generate_password()

    def show_passwords(self, temp_key, tree):
        try:
            temp_fernet = get_fernet(temp_key)
            records = database.get_raw_passwords()
            for item in tree.get_children():
                tree.delete(item)
            for ide, site, enc_user, enc_pass in records:
                try:
                    username = temp_fernet.decrypt(enc_user).decode()
                    password = temp_fernet.decrypt(enc_pass).decode()
                    tree.insert("", "end", values=(ide, site, username, password))
                except Exception:
                    continue
        except Exception:
            messagebox.showerror("Error", "Incorrect master password or decryption error.")

    def populate_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        for ide, site, enc_user, _ in database.get_raw_passwords():
            try:
                username = self.fernet.decrypt(enc_user).decode()
                password = "********"
                tree.insert("", "end", values=(ide, site, username, password))
            except Exception:
                continue

    def copy_password(self, ide, site, username):
        _, _, _, enc_pass = database.get_raw_password(ide)
        password = self.fernet.decrypt(enc_pass).decode()
        pyperclip.copy(password)
        messagebox.showinfo("Copied", f"Site: {site}\nUsername: {username}\nPassword copied to clipboard.")
