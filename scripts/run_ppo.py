# In run_ppo.py
import pandas as pd
import torch
from portfolio_env import PortfolioEnv
from ppo_policy import PPOPolicyNetwork
from ppo_train import ppo_train

# Load the stock data (replace 'stock_data.csv' with the actual file path)
data = pd.read_csv(r'C:\Users\parth\Desktop\Projects\AI-Powered-Financial-Portfolio-Optimization\data\SPY_preprocessed_data.csv')

# Ensure only numerical columns are used (drop 'date' and 'ticker')
numerical_data = data[['shares_outstanding', 'nav', 'flow_daily']]  # Only numerical columns
env = PortfolioEnv(numerical_data)  # Use this filtered data in the environment

# Initialize the PPO agent
input_dim = len(numerical_data.columns)  # Number of numerical features (3 features)
output_dim = env.action_space.n  # Number of possible actions (Buy, Sell, Hold)
agent = PPOPolicyNetwork(input_dim, output_dim)

# Train the agent using PPO
ppo_train(agent, env)

# Save the trained agent (Optional, for later use)
torch.save(agent.state_dict(), 'ppo_agent.pth')
