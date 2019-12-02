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
        self.epsilon = 1.0 #exploration rate
        self.epsilon_decay = 0.996
        self.epsilon_min = 0.01
        self.gamma = 0.95 #discount rate
        self.image_size = image_size
        self.learn_count = 0
        self.num_actions = num_actions
        self.policy_network = Network(image_size, num_actions)
        self.target_network = Network(image_size, num_actions)
        self.target_network.weights = self.policy_network.weights
        self.replay_memory = ReplayMemory(capacity=50000)    

    def gather_experience(self, last_screenshot, action, reward, new_screenshot, done):
        self.replay_memory.write(last_screenshot, action, reward, new_screenshot, done)
        return

    def choose_action(self, observation):
        if np.random.rand() > self.epsilon:
            q_compute = self.policy_network.compute(np.array([observation]))
            return np.argmax(q_compute[0])
        else:
            return np.random.choice(range(self.num_actions))               

    def learn(self):
        batch = self.replay_memory.sample(self.batch_size)

        states = np.array([exp.start_state for exp in batch])
        current_q_values = np.array(self.policy_network.compute(states))

        next_states = np.array([exp.end_state for exp in batch])
        next_q_values = np.array(self.target_network.compute(next_states))

        x_batch = np.zeros([np.shape(batch)[0], self.image_size[0], self.image_size[1]])
        y_batch = np.zeros([np.shape(batch)[0], self.num_actions])

        for i in range(np.shape(batch)[0]):
            x_batch[i,:] = batch[i].start_state
            for j in range(self.num_actions):
                if j == batch[i].action:
                    if batch[i].done:
                        y_batch[i,j] = batch[i].reward
                    else:
                        y_batch[i,j] = batch[i].reward + self.gamma * np.max(next_q_values[i])
                else:
                    y_batch[i,j] = current_q_values[i,j]                    
        self.policy_network.train(train_samples=x_batch, train_labels=y_batch)

        self.learn_count +=1
        if (self.learn_count % 25) == 0:
            self.target_network.weights = self.policy_network.weights
            self.learn_count = 0

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay            
        
        return

    def loadModel(self, num_episodes):
        self.policy_network.load_weights(f'policy_network_weights_{num_episodes}')
        self.target_network.load_weights(f'policy_network_weights_{num_episodes}')
        return

    def saveModel(self, num_episodes):
        self.policy_network.save_weights(f'policy_network_weights_{num_episodes}')
        return

