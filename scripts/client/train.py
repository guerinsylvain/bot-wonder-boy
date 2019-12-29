import numpy as np
import sys
from lib.agent import DeepQLearningAgent
from lib.environment import Environment
from lib.experience import Experience

print(f'starting training')
accuracy = 0
num_actions = 5
num_episodes = 100000
environment = Environment()
agent = DeepQLearningAgent(environment.frameset_size, num_actions, environment.hot_encode_action_size)
agent.saveModel(0)
agent.loadModel('policy_network_model_0.h5')

for episode in range(1, num_episodes):

    done = 0
    rewards_current_episode = 0
    position_current_episode = 0
    level_position = 0
    last_frameset = np.zeros(environment.frameset_size) 
    last_last_actions = np.zeros(environment.hot_encode_action_size)
    environment.start()

    first_random_action = np.random.choice(range(agent.num_actions))
    environment.sendAction(first_random_action)
    reward, frameset, done, level_position, last_actions  = environment.getState()    
    agent.gather_experience(last_frameset, last_last_actions, first_random_action, reward, frameset, last_actions, done)
    last_frameset = frameset
    last_last_actions = last_actions
    rewards_current_episode += reward
    position_current_episode = max(position_current_episode, level_position)

    while done != 1:
        action = agent.choose_action(last_last_actions, last_frameset)
        environment.sendAction(action)
        reward, frameset, done, level_position, last_actions  = environment.getState()    
        agent.gather_experience(last_frameset, last_last_actions, action, reward, frameset, last_actions, done)
        accuracy = agent.learn()
        last_frameset = frameset
        rewards_current_episode += reward    
        position_current_episode = max(position_current_episode, level_position)
        print(f'episode {episode:0>4d}, level position: {(position_current_episode/81.60):.2f}, episode reward: {rewards_current_episode}, e: {agent.epsilon:.2f}, acc:{accuracy:.3f}     ', end = '\r')
    
    if (episode % 100) == 0:
        agent.saveModel(episode)

    print(f'episode {episode:0>4d}, level position: {(position_current_episode/81.60):.2f}, episode reward: {rewards_current_episode}, e: {agent.epsilon:.2f}, acc:{accuracy:.3f}     ')
environment.exit()
