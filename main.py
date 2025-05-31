import tkinter as tk
from tkinter import messagebox, simpledialog
from app import PasswordManagerApp
from gui import PasswordManagerGUI

def main():
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal momentáneamente
    master_key = simpledialog.askstring("Master Key", "Enter your master key:", show="*")
    if not master_key:
        messagebox.showerror("Error", "Master key is required.")
        return
    try:
        app = PasswordManagerApp(master_key)
    except ValueError as e:
        messagebox.showerror("Weak Key", str(e))
        return
    root.deiconify()  # Mostrar ventana principal
    gui = PasswordManagerGUI(root, app)
    root.mainloop()

if __name__ == "__main__":
    main()
