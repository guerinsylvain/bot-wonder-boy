import sys
from lib.agent import Agent
from lib.environment import Environment
from lib.experience import Experience

print(f'starting training')
num_actions = 12
num_episodes = 1000
agent = Agent(num_actions)
environment = Environment()

for episode in range(num_episodes):

    print(f'starting episode {episode}')
    done = 0
    rewards_current_episode = 0
    environment.start()

    while done != 1:
        action = agent.choose_action()
        environment.sendAction(action)
        reward, screenshot, done = environment.getState()    
        rewards_current_episode += reward    
        print(f'episode reward: {rewards_current_episode}', end = '\r')
environment.exit()
