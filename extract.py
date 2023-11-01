import requests
import os
from dotenv import load_dotenv
import pandas as pd

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
        "interval": 600,  # 10 minutes in seconds
        "duration": 2592000  # 30 days in seconds
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
    api_secret, mining_user_name, currency = initialize_environment()
    
    # Fetch the account hashrate history
    history = fetch_account_hashrate_history(api_secret, mining_user_name, currency)
    if history:
        history_df = pd.json_normalize(history, 'history')
        print("Hashrate History DataFrame:")
        history_df_filtered = history_df[['timestamp', 'hash_rate', 'online_miners']]
        print(history_df_filtered)
        print(history_df_filtered.shape)

    # Fetch the transactions list
    transactions = fetch_transactions_list(api_secret, mining_user_name, currency)
    if transactions:
        transactions_df = pd.json_normalize(transactions, 'transactions')
        print("Transactions List DataFrame:")
        transactions_df_filtered = transactions_df[['changed_balance', 'created_at']]
        print(transactions_df_filtered)
        print(transactions_df_filtered.shape)

    