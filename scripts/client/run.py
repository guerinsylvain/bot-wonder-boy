import numpy as np
from numpy import savetxt
import sys
from lib.agent import DeepQLearningAgent
from lib.environment import Environment
from lib.experience import Experience

print(f'starting run')
accuracy = 0
num_actions = 5
num_episodes = 100
environment = Environment(gray_scale = True)
agent = DeepQLearningAgent(environment.frameset_size, num_actions)
print(sys.argv[1])
agent.loadModel(sys.argv[1])
positions = []

for episode in range(num_episodes):

    print(f'starting episode {episode}')
    done = 0
    rewards_current_episode = 0
    position_current_episode = 0
    level_position = 0
    last_frameset = np.zeros(environment.frameset_size) 
    environment.start()

    first_random_action = np.random.choice(range(agent.num_actions))
    environment.sendAction(first_random_action)
    reward, frameset, done, level_position = environment.getState()    
    agent.gather_experience(last_frameset, first_random_action, reward, frameset, done)
    last_frameset = frameset
    rewards_current_episode += reward
    position_current_episode = max(position_current_episode, level_position)

    while done != 1:
        action = agent.choose_action(last_frameset, use_exploration=False)
        environment.sendAction(action)
        reward, frameset, done, level_position = environment.getState()    
        agent.gather_experience(last_frameset, action, reward, frameset, done)
        last_frameset = frameset
        rewards_current_episode += reward    
        position_current_episode = max(position_current_episode, level_position)
        print(f'episode {episode:0>4d}, level position: {position_current_episode:0>2d}/32, episode reward: {rewards_current_episode}, e: {agent.epsilon:.2f}     ', end = '\r')
    
    print(f'episode {episode:0>4d}, level position: {position_current_episode:0>2d}/32, episode reward: {rewards_current_episode}, e: {agent.epsilon:.2f}     ')
    positions.append(position_current_episode)  
    if episode == 100:  
        savetxt(f'{episode}.csv', np.array(positions), delimiter=',')
environment.exit()
