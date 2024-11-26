import os
import pandas as pd
import requests
from dotenv import load_dotenv

# Load environment variables (API key should be stored in .env)
load_dotenv()

NASDAQ_API_KEY = os.getenv("NASDAQ_API_KEY")

def fetch_data(ticker):
    """
    Fetch ETF data from Nasdaq API for a specific ticker.
    """
    url = f"https://data.nasdaq.com/api/v3/datatables/ETFG/FUND.json?ticker={ticker}&api_key={NASDAQ_API_KEY}"
    try:
        # Send GET request to fetch the data
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Extract JSON data from the response
        data = response.json()

        # Check if the 'datatable' key exists and if it contains data
        if 'datatable' in data and 'data' in data['datatable']:
            # Extract the data and the columns
            data_list = data['datatable']['data']
            columns = data['datatable']['columns']  # The columns are provided in the 'columns' key

            # Create a DataFrame
            df = pd.DataFrame(data_list, columns=[col['name'] for col in columns])
            return df
        else:
            print("Error: Data not available.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def save_to_csv(data, filename):
    """
    Save a DataFrame to a CSV file.
    """
    if data is not None:
        data.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print("No data to save.")

def main():
    # Ticker and date range (API will handle the rest)
    ticker = "SPY"  # Example ETF ticker
    
    # Fetch the data from Nasdaq
    print(f"Fetching data for {ticker}...")
    raw_data = fetch_data(ticker)
    
    # Save the data to CSV
    if raw_data is not None:
        output_path = "../data/spy_etf_data.csv"
        save_to_csv(raw_data, output_path)
    else:
        print("No data fetched for ticker.")

if __name__ == "__main__":
    main()
