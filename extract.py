import requests
import os
from dotenv import load_dotenv
import pandas as pd
import logging
import storage
import external

def initialize_environment():
    """Load environment variables and return necessary configurations."""
    load_dotenv()
    api_secret = os.getenv("F2POOL_API_SECRET")
    mining_user_name = os.getenv("MINING_USER_NAME")
    currency = os.getenv("CURRENCY")
    return api_secret, mining_user_name, currency

def post_to_f2pool(api_secret, endpoint, additional_data={}):
    """Post a request to the f2pool API."""
    # API endpoint
    url = f"https://api.f2pool.com/v2/{endpoint}"
    
    # Request headers
    headers = {
        'Content-Type': 'application/json',
        'F2P-API-SECRET': api_secret
    }
    
    # Ensure that 'currency' and 'mining_user_name' are included in the payload
    if 'currency' not in additional_data or not additional_data['currency']:
        raise ValueError("The 'currency' parameter must be provided and non-empty.")
    if 'mining_user_name' not in additional_data or not additional_data['mining_user_name']:
        raise ValueError("The 'mining_user_name' parameter must be provided and non-empty.")
    
    # Make the POST request
    response = requests.post(url, headers=headers, json=additional_data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None
    
def fetch_account_hashrate_history(api_secret, mining_user_name, currency):
    """Fetch the historical hashrate data for the given mining user name and currency."""
    endpoint = "hash_rate/history"
    
    # Additional data required for the request
    payload = {
        "mining_user_name": mining_user_name,
        "currency": currency,
        "interval": 600,  # 10 minutes in seconds (granularity)
        "duration": 2592000  # 30 days in seconds (data for past 30 days)
    }
    # Return the response
    return post_to_f2pool(api_secret, endpoint, payload)    
    

def fetch_transactions_list(api_secret, mining_user_name, currency, transaction_type="all"):
    """Fetch all transactions for the given mining user name and currency."""
    endpoint = "assets/transactions/list"
    additional_data = {
        "mining_user_name": mining_user_name,
        "currency": currency,                  
        "type": transaction_type
    }
    return post_to_f2pool(api_secret, endpoint, additional_data)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Initialize the database and create tables if they don't exist
    storage.create_tables()

    api_secret, mining_user_name, currency = initialize_environment()

    # Fetch the account hashrate history
    history = fetch_account_hashrate_history(api_secret, mining_user_name, currency)
    if history:
        history_df = pd.json_normalize(history, 'history')
        print("Hashrate History DataFrame:")
        history_df_filtered = history_df[['timestamp', 'hash_rate', 'online_miners']]
        print(history_df_filtered)
        print(history_df_filtered.shape)
        storage.insert_hashrate_history(history_df_filtered)
        logging.info(f"Data inserted into the database at {storage.DATABASE_FILEPATH}")

    # Get timestamps and records from the database
    timestamp_records = storage.get_timestamps_and_records()

    # Fetch and update difficulty and price for each timestamp, if necessary
    for timestamp, difficulty, price in timestamp_records:
        if difficulty is None or price is None:
            difficulty, price = external.fetch_closest_difficulty_and_price_for_timestamp(int(timestamp))
            storage.update_difficulty_and_price(timestamp, difficulty, price)
            logging.info(f"Updated difficulty and price for timestamp {timestamp}.")
        else:
            logging.info(f"Difficulty and price already recorded for timestamp {timestamp}.")

    # Fetch the transactions list
    transactions = fetch_transactions_list(api_secret, mining_user_name, currency)
    if transactions:
        transactions_df = pd.json_normalize(transactions, 'transactions')
        print("Transactions List DataFrame:")
        transactions_df_filtered = transactions_df[['changed_balance', 'created_at']]
        print(transactions_df_filtered)
        print(transactions_df_filtered.shape)