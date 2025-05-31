import sqlite3

def get_connection():
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row  # Enables dict-like row access
    return conn
