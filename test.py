import quandl

# Set the correct API key directly
quandl.ApiConfig.api_key = "DvNHJxfE5GMixyuXjQuk"  # Replace with your actual API key

# Test fetching data
try:
    data = quandl.get("WIKI/AAPL", start_date="2023-01-01", end_date="2023-12-31")
    print(data.head())
except Exception as e:
    print(f"Error: {e}")

