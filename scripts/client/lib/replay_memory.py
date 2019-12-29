from lib.experience import Experience
import random
from typing import List

class ReplayMemory:
    def __init__(self, capacity):
        self.__memory = []
        self.__push_count = 0
        self.__capacity = capacity

    def write(self, initial_frameset, initial_last_actions, action, reward, new_frameset, new_last_actions, done):
        experience = Experience(initial_frameset, initial_last_actions, action, reward, new_frameset, new_last_actions, done)
        if len(self.__memory) < self.__capacity:
            self.__memory.append(experience)
        else:
            self.__memory[self.__push_count % self.__capacity] = experience
        self.__push_count += 1

    def sample(self, batch_size) -> List[Experience]:
        if len(self.__memory) > batch_size:
            last_exp = self.__memory[:1][0]
            sample = random.sample(self.__memory, batch_size-1)
            sample.append(last_exp)
            return sample
        else:
            return random.sample(self.__memory, len(self.__memory))