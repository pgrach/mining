from datetime import datetime, timezone
import requests

def fetch_closest_difficulty_and_price_for_timestamp(target_timestamp):
    """Fetch the closest difficulty and BTC price for a specific timestamp."""

    def convert_to_unix_timestamp(date_string):
        try:
            dt = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            dt = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
        return int(dt.replace(tzinfo=timezone.utc).timestamp())
    
    # API endpoint
    url = "https://insights.braiins.com/api/v1.0/hashrate-and-difficulty-history"
    
    # Parameters
    params = {"timeframe": "all"}  # You can adjust this based on how much history you want
    
    # Fetch data from API
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    # Find the closest timestamp in the returned data
    closest_difficulty = None
    closest_price = None
    closest_timestamp = None
    min_diff = float('inf')
    for entry in data['difficulty']:
        diff = abs(convert_to_unix_timestamp(entry['x']) - target_timestamp)
        if diff < min_diff:
            min_diff = diff
            closest_difficulty = entry['y']
            closest_timestamp = entry['x']

    # Find the BTC price for the closest timestamp
    for entry in data['price']:
        if entry['x'] == closest_timestamp:
            closest_price = entry['y']
            break
    
    return closest_difficulty, closest_price

# Example usage
timestamp = 1696260600  # Replace this with your specific timestamp
difficulty, price = fetch_closest_difficulty_and_price_for_timestamp(timestamp)
print(f"Closest difficulty to timestamp {timestamp}: {difficulty}")
print(f"BTC price at that time: {price}")