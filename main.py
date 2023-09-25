import requests
import json
import time
from datetime import datetime

API_BASE_URL = "https://api.f2pool.com/v2"

# Load the API secret from a config.json file:
with open('config.json', 'r') as f:
    config = json.load(f)
API_SECRET = config["F2P_API_SECRET"]

# Define the headers required for the API request:
HEADERS = {
    'Content-Type': 'application/json',
    'F2P-API-SECRET': API_SECRET
}

def get_hashrate_history(mining_user_name, currency, start_time, end_time):
    endpoint = f"{API_BASE_URL}/hash_rate/history"
    
    # We're setting the interval to 3600 seconds for hourly data
    payload = {
        "mining_user_name": mining_user_name,
        "currency": currency,
        "interval": 3600,
        "duration": end_time - start_time
    }

    response = requests.post(endpoint, headers=HEADERS, json=payload)
    if response.status_code == 200:
        data = response.json()
        if "history" in data:
            return data["history"]
        else:
            print(f"Unexpected data received: {data}")
            return None
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# Define the start and end times for Aug
start_time = int(time.mktime(datetime(2023, 9, 20).timetuple()))
end_time = int(time.mktime(datetime(2023, 9, 21).timetuple()))

# Fetch the hashrate history for Aug
username = "sgkpg"
currency = "bitcoin"
hashrate_history = get_hashrate_history(username, currency, start_time, end_time)

if hashrate_history:
    # Print the fetched hashrate data for Aug
    for entry in hashrate_history:
        timestamp = datetime.utcfromtimestamp(entry["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')
        hashrate = entry["hash_rate"]
        print(f"Timestamp: {timestamp}, Hashrate: {hashrate} H/s")
else:
    print("Failed to retrieve hashrate history.")