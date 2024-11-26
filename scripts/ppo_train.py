import matplotlib.pyplot as plt
import torch

def ppo_train(agent, env, episodes=10000):
    episode_rewards_list = []  # List to store the total rewards for each episode

    for episode in range(episodes):
        state = env.reset()
        done = False
        episode_rewards = 0

        while not done:
            # Get the action, log probability, and entropy from the agent
            action, log_prob, entropy = agent.select_action(state)
            
            # Take the action in the environment
            next_state, reward, done, _ = env.step(action)
            
            # Learn from the experience
            agent.learn(state, action, reward, next_state, done)

            state = next_state
            episode_rewards += reward
        
        episode_rewards_list.append(episode_rewards)  # Store reward for this episode
        print(f"Episode {episode+1}: Total Reward = {episode_rewards}")
    
    #After training, plot the reward
    plt.plot(episode_rewards_list)
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.title("PPO Training Rewards Over Time")
    plt.show()
    # At the end of training, save the trained model
    torch.save(agent.state_dict(), 'ppo_agent.pth')

