import sqlite3


# Create the database and the passwords table if it doesn't exist
def create_db(db_name="passwords.db"):
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site TEXT NOT NULL,
                username BLOB NOT NULL,
                password BLOB NOT NULL
            )
        """)

# Insert a new password entry, encrypting the username and password
def insert_password(site, username, password, fernet, db_name="passwords.db"):
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO passwords (site, username, password) VALUES (?, ?, ?)",
                  (site, fernet.encrypt(username.encode()), fernet.encrypt(password.encode())))
        conn.commit()

# Retrieve and decrypt all stored passwords
def get_passwords(fernet, db_name="passwords.db"):
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        c.execute("SELECT site, username, password FROM passwords")
        return [(site, fernet.decrypt(user).decode(), fernet.decrypt(pwd).decode())
                for site, user, pwd in c.fetchall()]

# Retrieve all password entries without decrypting (used for later decryption)
def get_raw_passwords():
    with sqlite3.connect("passwords.db") as conn:
        c = conn.cursor()
        c.execute("SELECT site, username, password FROM passwords")
        return c.fetchall()

# Insert a new password entry, encrypting the username and password
def insert_password(site, username, password, fernet):
    with sqlite3.connect("passwords.db") as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                site TEXT,
                username BLOB,
                password BLOB
            )
        ''')
        c.execute('''
            INSERT INTO passwords (site, username, password)
            VALUES (?, ?, ?)
        ''', (site, fernet.encrypt(username.encode()), fernet.encrypt(password.encode())))
        conn.commit()