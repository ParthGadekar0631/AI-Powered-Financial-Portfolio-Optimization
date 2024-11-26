import pandas as pd
import torch
import matplotlib.pyplot as plt
from portfolio_env import PortfolioEnv
from ppo_policy import PPOPolicyNetwork

# Load the evaluation data
data = pd.read_csv(r'C:\Users\parth\Desktop\Projects\AI-Powered-Financial-Portfolio-Optimization\data\SPY_preprocessed_data.csv')
numerical_data = data[['shares_outstanding', 'nav', 'flow_daily']]
env = PortfolioEnv(numerical_data)

# Load the trained model
input_dim = len(numerical_data.columns)
output_dim = env.action_space.n
agent = PPOPolicyNetwork(input_dim, output_dim)
agent.load_state_dict(torch.load(
    r'C:\Users\parth\Desktop\Projects\AI-Powered-Financial-Portfolio-Optimization\scripts\ppo_agent.pth',
    weights_only=True
))

# Evaluate the model
state = env.reset()
done = False
cumulative_rewards = []
actions_taken = []
step = 0
total_reward = 0

while not done:
    action, _, _ = agent.select_action(state)
    next_state, reward, done, _ = env.step(action)
    total_reward += reward
    cumulative_rewards.append(total_reward)
    actions_taken.append(action)
    state = next_state
    step += 1

# Visualization
# 1. Cumulative Rewards Over Steps
plt.figure(figsize=(10, 6))
plt.plot(cumulative_rewards, label="Cumulative Rewards")
plt.xlabel("Steps")
plt.ylabel("Cumulative Reward")
plt.title("Cumulative Rewards Over Time")
plt.legend()
plt.grid(True)
plt.savefig("cumulative_rewards.png")  # Save as an image
plt.show()

# 2. Actions Distribution (Histogram)
plt.figure(figsize=(8, 5))
plt.hist(actions_taken, bins=3, edgecolor='k', align='mid', rwidth=0.6)
plt.xticks([0, 1, 2], ["Buy", "Sell", "Hold"])
plt.xlabel("Actions")
plt.ylabel("Frequency")
plt.title("Distribution of Actions Taken")
plt.grid(True)
plt.savefig("actions_distribution.png")  # Save as an image
plt.show()
