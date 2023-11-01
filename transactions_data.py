import pandas as pd
from common import initialize_environment, post_to_f2pool

def fetch_transaction_data(api_secret, mining_user_name, currency, transaction_type="all"):
    """Fetch the transaction data for the given user and currency."""
    return post_to_f2pool(api_secret, mining_user_name, currency, "assets/transactions/list", {"type": transaction_type})

def main():
    """Main function to handle the execution flow."""
    api_secret, mining_user_name, currency = initialize_environment()
    transaction_data = fetch_transaction_data(api_secret, mining_user_name, currency)

    # Convert the transactions list into a pandas DataFrame
    df = pd.DataFrame(transaction_data['transactions'])
    
    # Convert the Unix epoch timestamps in the 'created_at' column to human-readable date and time
    df['created_at'] = pd.to_datetime(df['created_at'], unit='s')
    
    # Display the entire DataFrame
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df)
    
    # Determine and display the earliest and latest dates
    earliest_date = df['created_at'].min()
    latest_date = df['created_at'].max()
    
    print(f"\nThe earliest transaction date is: {earliest_date}")
    print(f"The latest transaction date is: {latest_date}")

if __name__ == "__main__":
    main()