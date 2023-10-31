import requests
import os
from dotenv import load_dotenv

def initialize_environment():
    """Load environment variables and return necessary configurations."""
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve values from the environment variables
    api_secret = os.getenv("F2POOL_API_SECRET")
    mining_user_name = os.getenv("MINING_USER_NAME")
    currency = os.getenv("CURRENCY")

    return api_secret, mining_user_name, currency

def fetch_hashrate_info(api_secret, mining_user_name, currency):
    """Fetch the hashrate information for the given user and currency."""
    # API endpoint
    url = f"https://api.f2pool.com/v2/hash_rate/info"
    
    # Request headers
    headers = {
        'Content-Type': 'application/json',
        'F2P-API-SECRET': api_secret
    }
    
    # Request payload
    data = {
        "mining_user_name": mining_user_name,
        "currency": currency
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def main():
    """Main function to handle the execution flow."""
    api_secret, mining_user_name, currency = initialize_environment()
    mining_performance_data = fetch_hashrate_info(api_secret, mining_user_name, currency)
    print(mining_performance_data)

if __name__ == "__main__":
    main()