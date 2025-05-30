# Pyssword_Manager
## 🔐 Password Manager in Python (Tkinter + SQLite + Cryptography)

This is a simple password manager built with Python and a graphical user interface using `tkinter`. Passwords and usernames are individually encrypted using the `cryptography` library and stored in a local SQLite database. This is ideal as a personal project or learning tool about GUI design, basic security, and secure local storage.

## ✨ Features

- User-friendly GUI built with `tkinter`
- Field-level encryption for sensitive data (`username` and `password`) using a master key
- Local storage in SQLite
- Secure password generation
- Automatic copy to clipboard
- Secure viewing of stored entries
- Modular code organized into multiple files

## 📁 Project Structure

```
pyssword_manager/
│
├── crypto.py              # Encryption and key derivation functions
├── database.py            # SQLite database operations
├── password_generator.py  # Secure password generator
├── main.py                # Main GUI using tkinter
├── requirements.txt       # Project dependencies
├── salt.bin               # Persistent salt for key derivation
└── passwords.db           # Local database (auto-generated)

````

## ⚙️ Requirements

- Python 3.8 or later
- pip

## 📦 Installation

1. Clone or download this repository.
2. Install the required packages:

```bash
pip install -r requirements.txt
````

## 🚀 Usage

1. Run the program:

```bash
python main.py
```

2. On startup, enter a **master key**. This will be used to encrypt and decrypt the data. **Do not forget it!**

3. Through the interface you can:

   * Enter a site, username, and password.
   * Generate secure random passwords (automatically copied to clipboard).
   * View stored entries (requires same master key used when saving).

## 🔐 Security

* Passwords and usernames are encrypted with `Fernet` (symmetric encryption) using a key derived from the user-provided master key.
* Key derivation uses PBKDF2 with SHA-256 and a `salt` stored in `salt.bin`.
* The database is not fully encrypted, but sensitive fields are.

## 🔑 Master Key Considerations

The **master key is critical** to accessing your encrypted data. Since encryption and decryption are performed using a key derived from this password:

* **Choose a strong, unique master key** that you can remember.
* **Do not share it** and **do not lose it** — if forgotten, the encrypted data cannot be recovered.
* Consider using a phrase or pass-sentence instead of a single word for increased security.

## ☁️ Use in the Cloud

Although the password database is stored locally, you can:

* **Place the project folder inside a cloud-synced directory** (like Google Drive, Dropbox, or OneDrive).
* This way, you can **access your passwords from any computer**, as long as you have:

  * Python installed
  * The required packages (`requirements.txt`)
  * The same `salt.bin` file and database
  * Your **master key**

⚠️ Make sure to secure your cloud account and local machines. This app **does not use two-factor authentication** or remote access restrictions.

## 🧪 Dependencies

* `cryptography`: for secure encryption/decryption.
* `pyperclip`: to copy passwords to clipboard.
* `tkinter`: comes pre-installed with most Python distributions.

## 🛠️ Possible Improvements

* Support for updating or deleting entries.
* Search functionality by site.
* Export encrypted data.
* Full database encryption (e.g., using SQLCipher).

## 📜 License

This project is licensed under the **GNU General Public License v3.0 (GPLv3)**. This means the code will **always remain open source**, and any modifications or distributions must also be shared under the same license. The GPL ensures that the freedom to use, modify, and share the software is preserved for everyone.

---

**Developed by:** Sergio A. Hernandez
