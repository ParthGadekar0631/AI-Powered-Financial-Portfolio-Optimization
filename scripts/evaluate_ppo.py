import pandas as pd
import torch
from portfolio_env import PortfolioEnv
from ppo_policy import PPOPolicyNetwork

# Load the trained PPO agent
agent = PPOPolicyNetwork(input_dim=3, output_dim=3)  # Same dimensions as during training
agent.load_state_dict(torch.load(r'C:\Users\parth\Desktop\Projects\AI-Powered-Financial-Portfolio-Optimization\scripts\ppo_agent.pth', weights_only=True))

# Load the test data (you can use a different or unseen portion of the data)
data = pd.read_csv(r'C:\Users\parth\Desktop\Projects\AI-Powered-Financial-Portfolio-Optimization\data\SPY_preprocessed_data.csv')

# Filter the numerical columns (only the ones used during training)
numerical_data = data[['shares_outstanding', 'nav', 'flow_daily']]

# Initialize the environment with the test data
env = PortfolioEnv(numerical_data)

# Run the agent in the environment and evaluate its performance
state = env.reset()
done = False
total_reward = 0

while not done:
    action, _, _ = agent.select_action(state)  # Get the action from the trained agent
    next_state, reward, done, _ = env.step(action)  # Take the action in the environment
    state = next_state
    total_reward += reward  # Track the total reward

print(f"Total Reward from Evaluation = {total_reward}")
