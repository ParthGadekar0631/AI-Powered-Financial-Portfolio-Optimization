import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

class PPOPolicyNetwork(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(PPOPolicyNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.policy_head = nn.Linear(128, output_dim)  # Output for action probabilities (for Discrete actions)
        self.value_head = nn.Linear(128, 1)  # Output for value estimation
        
        # Define optimizer
        self.optimizer = optim.Adam(self.parameters(), lr=0.0003)
    
    def forward(self, state):
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))
        action_probs = torch.softmax(self.policy_head(x), dim=-1)  # Softmax for probability distribution
        value = self.value_head(x)  # State value estimation
        return action_probs, value
    
    def select_action(self, state):
        # Convert state to torch tensor
        state = torch.tensor(state, dtype=torch.float32).unsqueeze(0)  # Add batch dimension
        action_probs, _ = self.forward(state)
        dist = torch.distributions.Categorical(action_probs)
        action = dist.sample()  # Sample an action based on the probabilities
        return action.item(), dist.log_prob(action), dist.entropy()


    def learn(self, state, action, reward, next_state, done, gamma=0.99, epsilon=0.2, lam=0.95):
        # Convert states and actions to tensors
        state = torch.tensor(state, dtype=torch.float32).unsqueeze(0)  # Add batch dimension
        next_state = torch.tensor(next_state, dtype=torch.float32).unsqueeze(0)  # Add batch dimension
        action = torch.tensor(action, dtype=torch.long).unsqueeze(0)
        reward = torch.tensor(reward, dtype=torch.float32).unsqueeze(0)
        done = torch.tensor(done, dtype=torch.float32).unsqueeze(0)
    
        # Get current value and next value estimates
        action_probs, value = self.forward(state)
        _, next_value = self.forward(next_state)
    
        # Calculate advantage using Generalized Advantage Estimation (GAE)
        td_error = reward + (1 - done) * gamma * next_value - value
        advantage = td_error.detach()  # For simplicity, using TD error as advantage (you can enhance this with GAE)

        # Compute the ratio (for clipping in PPO)
        dist = torch.distributions.Categorical(action_probs)
        log_prob = dist.log_prob(action)
        ratio = torch.exp(log_prob - action)  # New probability / old probability

        # Compute surrogate loss (clipped PPO objective)
        surrogate_loss = torch.min(ratio * advantage, 
                               torch.clamp(ratio, 1 - epsilon, 1 + epsilon) * advantage)

        # Compute value loss (mean squared error)
        value_loss = F.mse_loss(value, reward + (1 - done) * gamma * next_value)

        # Compute entropy loss to encourage exploration
        entropy_loss = dist.entropy().mean()

        # Total loss (combine policy loss, value loss, and entropy loss)
        total_loss = -surrogate_loss.mean() + 0.5 * value_loss - 0.01 * entropy_loss

        # Backpropagate and update the policy
        self.optimizer.zero_grad()
        total_loss.backward()
        self.optimizer.step()

