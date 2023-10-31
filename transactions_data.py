from common import initialize_environment, post_to_f2pool


def fetch_transaction_data(api_secret, mining_user_name, currency, transaction_type="all"):
    """Fetch the transaction data for the given user and currency."""
    return post_to_f2pool(api_secret, mining_user_name, currency, "assets/transactions/list", {"type": transaction_type})

def main():
    """Main function to handle the execution flow."""
    api_secret, mining_user_name, currency = initialize_environment()
    transaction_data = fetch_transaction_data(api_secret, mining_user_name, currency)
    print(transaction_data)

if __name__ == "__main__":
    main()