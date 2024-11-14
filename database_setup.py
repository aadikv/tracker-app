import sqlite3

def create_database():
    conn = sqlite3.connect('expiration_tracker.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            expiration_date DATE,
            notify_date DATE,
            device_token TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_database()