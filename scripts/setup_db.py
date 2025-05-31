from lib.db.connection import get_connection

def setup():
    with open("lib/db/schema.sql", "r") as f:
        schema = f.read()
    with get_connection() as conn:
        conn.executescript(schema)
        print("Database setup complete.")

if __name__ == "__main__":
    setup()
