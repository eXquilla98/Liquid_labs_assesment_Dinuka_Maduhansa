import sqlite3
DB_name = "market_data.db"


def get_db_connection():
    conn = sqlite3.connect(DB_name)
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monthly_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            volume INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
