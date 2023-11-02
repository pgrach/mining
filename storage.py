import os
import sqlite3

DATABASE_FILENAME = 'mining_data.db'
DATABASE_FILEPATH = os.path.join(os.getcwd(), DATABASE_FILENAME)

def connect():
    """Create and return a database connection."""
    return sqlite3.connect(DATABASE_FILEPATH)

def create_tables():
    """Create tables in the database if they don't exist."""
    with connect() as conn:
        cursor = conn.cursor()
        create_hashrate_table_query = """
            CREATE TABLE IF NOT EXISTS hashrate_history (
                timestamp TEXT NOT NULL,
                hash_rate REAL NOT NULL,
                online_miners INTEGER NOT NULL
            );
        """
        cursor.execute(create_hashrate_table_query)
        conn.commit()

def insert_hashrate_history(df):
    """Insert hashrate history data into the database."""
    with connect() as conn:
        df.to_sql('hashrate_history', conn, if_exists='append', index=False)

def main():
    """Main function to create tables when this script runs."""
    create_tables()

if __name__ == "__main__":
    main()
