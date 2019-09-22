from lib.agent import Agent
from lib.environment import Environment

num_actions = 12
agent = Agent(num_actions)
environment = Environment()

done = 0
environment.start()

while done != 1:
    action = agent.choose_action()
    environment.sendAction(action)
    reward, done = environment.getState()

environment.exit()
