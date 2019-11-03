from lib.network import Network
import numpy as np
import random
from lib.replay_memory import ReplayMemory

# default agent with random action policy
class Agent:
    def __init__(self, num_actions):
        # 12 possible actions
        self.num_actions = num_actions

    def choose_action(self, observation):
        # default implementation is to choose a random action
        return np.random.choice(range(self.num_actions))

    def gather_experience(self, last_screenshot, action, reward, new_screenshot):
        return

    def learn(self):
        return

# agent with deep Q learning
class DeepQLearningAgent(Agent):
    def __init__(self, image_size, num_actions):
        super().__init__( num_actions)
        self.batch_size = 150
        self.epsilon = 0.05
        self.gamma = 0.9
        self.image_size = image_size
        self.num_actions = num_actions
        self.q = Network(image_size, num_actions)
        self.replay_memory = ReplayMemory(capacity=50000)        

    def gather_experience(self, last_screenshot, action, reward, new_screenshot):
        self.replay_memory.write(last_screenshot, action, reward, new_screenshot)
        return

    def choose_action(self, observation):
        if np.random.rand() > self.epsilon:
            q_compute = self.q.compute(np.array([observation]))
            return np.argmax(q_compute[0])
        else:
            return np.random.choice(range(self.num_actions))               

    def learn(self):
        batch = self.replay_memory.sample(self.batch_size)

        last_states = np.array([exp.start_state for exp in batch])
        q_last_states = np.array(self.q.compute(last_states))

        next_states = np.array([exp.end_state for exp in batch])
        q_next_states = np.array(self.q.compute(next_states))

        x_batch = np.zeros([np.shape(batch)[0], self.image_size[0], self.image_size[1], self.image_size[2]])
        y_batch = np.zeros([np.shape(batch)[0], self.num_actions])

        for i in range(np.shape(batch)[0]):
            x_batch[i,:] = batch[i].start_state
            for j in range(self.num_actions):
                if j == batch[i].action:
                    y_batch[i,j] = batch[i].reward + self.gamma * np.max(q_next_states[i])
                else:
                    y_batch[i,j] = q_last_states[i,j]                    
        self.q.train(train_samples=x_batch, train_labels=y_batch)
        return
