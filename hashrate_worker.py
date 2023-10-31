import os
import requests
from dotenv import load_dotenv

def initialize_environment():
    """Load environment variables and return necessary configurations."""
    load_dotenv()
    api_secret = os.getenv("F2POOL_API_SECRET")
    mining_user_name = os.getenv("MINING_USER_NAME")
    currency = os.getenv("CURRENCY")
    return api_secret, mining_user_name, currency

def fetch_account_hashrate_history(api_secret, mining_user_name, currency):
    """Fetch the historical hashrate data for the given account."""
    url = "https://api.f2pool.com/v2/hash_rate/history"
    
    headers = {
        'Content-Type': 'application/json',
        'F2P-API-SECRET': api_secret
    }
    
    interval_seconds = 600  # 10 minutes in seconds
    duration_seconds = 30 * 24 * 60 * 60
    
    data = {
        "mining_user_name": mining_user_name,
        "currency": currency,
        "interval": interval_seconds,
        "duration": duration_seconds
    }
    
    response = requests.post(url, headers=headers, json=data)
    print(f"API Response Status Code: {response.status_code}")
    print(response.text)  # Print the server response
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    api_secret, mining_user_name, currency = initialize_environment()
    history = fetch_account_hashrate_history(api_secret, mining_user_name, currency)
    print(history)  # Print the JSON response