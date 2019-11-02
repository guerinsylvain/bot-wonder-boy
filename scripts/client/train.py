import numpy as np
import sys
from lib.agent import DeepQLearningAgent
from lib.environment import Environment
from lib.experience import Experience

print(f'starting training')
num_actions = 11
num_episodes = 1000
environment = Environment()
agent = DeepQLearningAgent(environment.image_size, num_actions)

for episode in range(num_episodes):

    print(f'starting episode {episode}')
    done = 0
    rewards_current_episode = 0
    last_screenshot = np.zeros(environment.image_size) 
    environment.start()

    first_random_action = np.random.choice(range(agent.num_actions))
    environment.sendAction(first_random_action)
    reward, screenshot, done = environment.getState()    
    agent.gather_experience(last_screenshot, first_random_action, reward, screenshot)
    last_screenshot = screenshot
    rewards_current_episode += reward

    while done != 1:
        action = agent.choose_action(last_screenshot)
        environment.sendAction(action)
        reward, screenshot, done = environment.getState()    
        agent.gather_experience(last_screenshot, action, reward, screenshot)
        agent.learn()
        last_screenshot = screenshot
        rewards_current_episode += reward    
        print(f'episode reward: {rewards_current_episode}', end = '\r')
    print(f'episode reward: {rewards_current_episode}')
environment.exit()
