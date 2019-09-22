import numpy as np
import random

# default agent with random action policy
class Agent:
    def __init__(self, num_actions):
        # 12 possible actions
        self.num_actions = num_actions

    def choose_action(self):
        # default implementation is to choose a random action
        return np.random.choice(range(self.num_actions))

# agent with deep Q learning
class DeepQLearningAgent(Agent):
    def __init__(self, num_actions):
        super().__init__( num_actions)
