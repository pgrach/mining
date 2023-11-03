import os
import sqlite3
import pandas as pd

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
                online_miners INTEGER NOT NULL,
                difficulty REAL,
                price REAL
            );
        """
        cursor.execute(create_hashrate_table_query)
        conn.commit()

def insert_hashrate_history(df):
    """Insert hashrate history data into the database."""
    with connect() as conn:
        df.to_sql('hashrate_history', conn, if_exists='append', index=False)

# retrieving the timestamp from db and storing difficulty and BTC price next to it

def get_timestamps_and_records():
    """Retrieve timestamps along with difficulty and price records from the database."""
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, difficulty, price FROM hashrate_history")
        return cursor.fetchall()
        
def update_difficulty_and_price(timestamp, difficulty, price):
    """Update the database with difficulty and BTC price for a specific timestamp."""
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE hashrate_history SET difficulty = ?, price = ? WHERE timestamp = ?",
            (difficulty, price, timestamp)
        )
        conn.commit()

def export_to_excel(filename='mining_data.xlsx'):
    """Export data from the database to an Excel file."""
    with connect() as conn:
        # Query the database
        query = "SELECT * FROM hashrate_history"
        df = pd.read_sql_query(query, conn)

        # Export to Excel
        df.to_excel(filename, index=False)
        print(f'Data exported to {filename}')

def main():
    """Main function to create tables when this script runs."""
    create_tables()

if __name__ == "__main__":
        export_to_excel()