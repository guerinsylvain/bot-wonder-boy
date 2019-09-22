from lib.agent import Agent
from lib.environment import Environment
from lib.experience import Experience

num_actions = 12
num_episodes = 1000
agent = Agent(num_actions)
environment = Environment()

for episode in range(num_episodes):

    done = 0
    environment.start()

    while done != 1:
        action = agent.choose_action()
        environment.sendAction(action)
        reward, done = environment.getState()

environment.exit()
