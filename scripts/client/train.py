import numpy as np
import sys
from lib.agent import DeepQLearningAgent
from lib.environment import Environment
from lib.experience import Experience

print(f'starting training')
num_actions = 5
num_episodes = 100000
environment = Environment(gray_scale = True)
agent = DeepQLearningAgent(environment.image_size, num_actions)

for episode in range(num_episodes):

    print(f'starting episode {episode}')
    done = 0
    rewards_current_episode = 0
    position_current_episode = 0
    level_position = 0
    last_screenshot = np.zeros(environment.image_size) 
    environment.start()

    first_random_action = np.random.choice(range(agent.num_actions))
    environment.sendAction(first_random_action)
    reward, screenshot, done, level_position = environment.getState()    
    agent.gather_experience(last_screenshot, first_random_action, reward, screenshot, done)
    last_screenshot = screenshot
    rewards_current_episode += reward
    position_current_episode = max(position_current_episode, level_position)

    while done != 1:
        action = agent.choose_action(last_screenshot)
        environment.sendAction(action)
        reward, screenshot, done, level_position = environment.getState()    
        agent.gather_experience(last_screenshot, action, reward, screenshot, done)
        agent.learn()
        last_screenshot = screenshot
        rewards_current_episode += reward    
        position_current_episode = max(position_current_episode, level_position)
        print(f'level position: {position_current_episode:0>2d}/32, episode reward: {rewards_current_episode}, e: {agent.epsilon:.2f}     ', end = '\r')
    
    if (episode % 100) == 0:
        agent.saveModel(episode)

    print(f'level position: {position_current_episode:0>2d}/32, episode reward: {rewards_current_episode}, e: {agent.epsilon:.2f}     ')
environment.exit()
