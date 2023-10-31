import json
import requests
import time
from datetime import datetime

# Define the start and end times for Aug
start_time = int(time.mktime(datetime(2023, 9, 20).timetuple()))
end_time = int(time.mktime(datetime(2023, 9, 21).timetuple()))


# Load the API secret from a config.json file:
with open('config.json', 'r') as f:
    config = json.load(f)
API_SECRET = config["F2P_API_SECRET"]

# Define the headers
HEADERS = {
    'F2P-API-SECRET': API_SECRET,
    'Content-Type': 'application/json'
}

mining_user_name = "sgkpg"

# Define the request payload
data = {
    "mining_user_name": mining_user_name,
    "currency": "bitcoin",
    "interval": 3600,
    "duration": end_time - start_time
}

# Make the request
response = requests.post('https://api.f2pool.com/v2/hash_rate/history', headers=HEADERS, json=data)

# Print the entire response
response_data = response.json()

print(response_data)
print("Timestamp\t\t\tHash Rate (H/s)\t\tOnline Miners")
print("---------------------------------------------------------")
for entry in response_data['history']:
    timestamp = datetime.fromtimestamp(entry['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
    
    # Format and round hash rate
    hash_rate = "{:,.2f}".format(entry['hash_rate'])
    
    # Number of online miners
    online_miners = entry['online_miners']
    
    print(f"{timestamp}\t{hash_rate}\t\t{online_miners}")
