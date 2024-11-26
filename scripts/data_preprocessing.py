import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# File path of the data (adjust the path if needed)
data_file = r"C:\Users\parth\Desktop\Projects\AI-Powered-Financial-Portfolio-Optimization\data\spy_etf_data.csv"

# Load the dataset
def load_data():
    data = pd.read_csv(data_file)
    return data

# Inspect the data (Check for missing values, data types)
def inspect_data(data):
    print("Data Inspection:\n")
    print(data.info())
    print("\nMissing Values:\n", data.isnull().sum())
    print("\nFirst few rows of data:\n", data.head())

# Handle missing values
def handle_missing_data(data):
    # Impute missing values with forward fill method (or use other strategies)
    data = data.fillna(method='ffill')
    return data

# Feature Engineering: Adding moving averages
# Feature Engineering: Adding moving averages
def add_technical_indicators(data):
    # Calculate the 50-day and 200-day moving averages of NAV
    data['50_day_MA'] = data['nav'].rolling(window=50).mean()
    data['200_day_MA'] = data['nav'].rolling(window=200).mean()
    return data


# Data Exploration: Visualize trends and correlations
# Data Exploration: Visualize trends and correlations
def data_exploration(data):
    # Convert 'date' and 'as_of_date' to datetime format
    data['date'] = pd.to_datetime(data['date'])
    data['as_of_date'] = pd.to_datetime(data['as_of_date'])

    plt.figure(figsize=(12, 6))
    
    # Plot NAV as a proxy for Close Price
    plt.subplot(1, 2, 1)
    plt.plot(data['date'], data['nav'], label='NAV')  # Use 'nav' instead of 'close'
    plt.title('SPY NAV over Time')
    plt.xlabel('Date')
    plt.ylabel('NAV')
    plt.xticks(rotation=45)
    
    # Plot Moving Averages
    plt.subplot(1, 2, 2)
    plt.plot(data['date'], data['50_day_MA'], label='50-Day MA')
    plt.plot(data['date'], data['200_day_MA'], label='200-Day MA')
    plt.title('SPY Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('NAV')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    # Compute the correlation matrix using only numeric columns
    numeric_data = data.select_dtypes(include=['float64', 'int64'])  # Select only numeric columns
    plt.figure(figsize=(8, 6))
    sns.heatmap(numeric_data.corr(), annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Matrix')
    plt.show()

# Main function to execute the steps
def main():
    # Load the data
    data = load_data()
    
    # Inspect the data
    inspect_data(data)
    
    # Handle missing values
    data = handle_missing_data(data)
    
    # Feature Engineering
    data = add_technical_indicators(data)
    
    # Data Exploration
    data_exploration(data)
    
    # Save the preprocessed data to a new file
    data.to_csv('../data/SPY_preprocessed_data.csv', index=False)
    print("\nPreprocessed data saved as 'SPY_preprocessed_data.csv'")

if __name__ == "__main__":
    main()
