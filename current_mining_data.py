import requests
from common import initialize_environment, post_to_f2pool

def fetch_hashrate_info(api_secret, mining_user_name, currency):
    """Fetch the hashrate information for the given user and currency."""
    return post_to_f2pool(api_secret, mining_user_name, currency, "hash_rate/info")

def main():
    """Main function to handle the execution flow."""
    api_secret, mining_user_name, currency = initialize_environment()
    mining_performance_data = fetch_hashrate_info(api_secret, mining_user_name, currency)
    print(mining_performance_data)

if __name__ == "__main__":
    main()