import requests
import json

API_BASE_URL = "https://api.f2pool.com/v2"
with open('config.json', 'r') as f:
    config = json.load(f)
API_SECRET = config["F2P_API_SECRET"]

HEADERS = {
    'Content-Type': 'application/json',
    'F2P-API-SECRET': API_SECRET
}


def get_hashrate(mining_user_name, currency):
    endpoint = f"{API_BASE_URL}/hash_rate/info"
    payload = {
        "mining_user_name": mining_user_name,
        "currency": currency
    }

    response = requests.post(endpoint, headers=HEADERS, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data["info"]
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


if __name__ == "__main__":
    username = input("Enter your mining username: ")
    currency = input("Enter the currency (e.g., bitcoin, ethereum): ")

    hashrate_info = get_hashrate(username, currency)
    if hashrate_info:
        print("\nHashrate Information:")
        print(f"Name: {hashrate_info['name']}")
        print(f"Current Hashrate: {hashrate_info['hash_rate']} H/s")
        print(f"Last 1 Hour Hashrate: {hashrate_info['h1_hash_rate']} H/s")
        print(f"Last 24 Hours Hashrate: {hashrate_info['h24_hash_rate']} H/s")
