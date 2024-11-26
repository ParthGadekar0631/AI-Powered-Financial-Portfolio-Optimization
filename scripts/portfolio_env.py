import gym
import numpy as np

class PortfolioEnv:
    def __init__(self, data):
        self.data = data
        self.current_step = 0
        self.action_space = gym.spaces.Discrete(3)  # Buy, Sell, Hold
    
    def reset(self):
        self.current_step = 0
        # Return only the numerical data (excluding 'date' and 'ticker')
        state = self.data.iloc[self.current_step][['shares_outstanding', 'nav', 'flow_daily']].values
        return state.astype(np.float32)  # Ensure state is float32
    
    def step(self, action):
        # If we're at the last step, set done to True
        if self.current_step >= len(self.data) - 1:
            done = True
        else:
            done = False

        # Here, you need to implement the logic for the reward and next_state.
        # Increment the current step
        self.current_step += 1
        
        # Ensure the next state is valid
        if self.current_step < len(self.data):
            next_state = self.data.iloc[self.current_step][['shares_outstanding', 'nav', 'flow_daily']].values
            next_state = next_state.astype(np.float32)
        else:
            next_state = np.zeros_like(self.data.iloc[0][['shares_outstanding', 'nav', 'flow_daily']].values)
            next_state = next_state.astype(np.float32)

        # Reward calculation: Currently using random values, should be replaced with actual logic
        reward = np.random.randn()  # Placeholder for your reward calculation
        
        return next_state, reward, done, {}
