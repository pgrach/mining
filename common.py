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

def post_to_f2pool(api_secret, mining_user_name, currency, endpoint, additional_data={}):
    """Post a request to the f2pool API."""
    # API endpoint
    url = f"https://api.f2pool.com/v2/{endpoint}"
    
    # Request headers
    headers = {
        'Content-Type': 'application/json',
        'F2P-API-SECRET': api_secret
    }
    
    # Default request payload
    data = {
        "mining_user_name": mining_user_name,
        "currency": currency
    }

    # Merge additional data into the default payload
    data.update(additional_data)
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

