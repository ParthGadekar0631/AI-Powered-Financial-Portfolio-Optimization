import yfinance as yf
import time
import torch
import pandas as pd
import numpy as np
from datetime import datetime
from ppo_policy import PPOPolicyNetwork

# Load the trained PPO agent
agent = PPOPolicyNetwork(input_dim=3, output_dim=3)  # Adjust input/output dims if needed
agent.load_state_dict(torch.load(r'C:\Users\parth\Desktop\Projects\AI-Powered-Financial-Portfolio-Optimization\scripts\ppo_agent.pth', weights_only=True))
agent.eval()  # Set the model to evaluation mode

# Function to fetch live data
def fetch_live_data(ticker):
    # Fetch data from Yahoo Finance
    stock = yf.Ticker(ticker)
    history = stock.history(period="1d", interval="1m")  # Last 1 day's data, 1-minute interval
    
    if history.empty:
        raise ValueError(f"No data fetched for {ticker}. Check ticker or API limits.")
    
    # For simplicity, generate placeholder values for `shares_outstanding` and `flow_daily`
    history['shares_outstanding'] = 1e6  # Example: Static value
    history['flow_daily'] = np.random.uniform(-1, 1, len(history))  # Example: Random flows
    
    # Keep only the necessary columns
    processed_data = history[['shares_outstanding', 'Close', 'flow_daily']].rename(columns={'Close': 'nav'})
    return processed_data.iloc[-1]  # Return the latest data point

# Function to preprocess and predict
def predict_action(data_row):
    state = data_row[['shares_outstanding', 'nav', 'flow_daily']].values.astype(np.float32)
    state = torch.tensor(state, dtype=torch.float32).unsqueeze(0)  # Add batch dimension
    action, _, _ = agent.select_action(state)
    return action

# Main deployment loop
def main():
    ticker = "SPY"  # Set the ticker symbol (SPY for SPDR S&P 500 ETF Trust)
    
    while True:
        try:
            # Step 1: Fetch the latest data
            live_data = fetch_live_data(ticker)
            print(f"Live Data at {datetime.now()}: {live_data.to_dict()}")
            
            # Step 2: Predict the action
            action = predict_action(live_data)
            actions = {0: "Buy", 1: "Sell", 2: "Hold"}
            print(f"Action: {actions[action]}")
            
            # Step 3: Log the action
            with open("action_log.txt", "a") as log_file:
                log_file.write(f"{datetime.now()}, {ticker}, {actions[action]}\n")
        
        except Exception as e:
            print(f"Error: {e}")
        
        # Fetch every 1 minute (adjust as needed)
        print("Waiting for the next update...")
        time.sleep(60)

if __name__ == "__main__":
    main()
