from lib.experience import Experience
import random
from typing import List

class ReplayMemory:
    def __init__(self, capacity):
        self.__memory = []
        self.__push_count = 0
        self.__capacity = capacity

    def write(self, initial_screenshot, action, reward, new_screenshot):
        experience = Experience(initial_screenshot, action, reward, new_screenshot)
        if len(self.__memory) < self.__capacity:
            self.__memory.append(experience)
        else:
            self.__memory[self.__push_count % self.__capacity] = experience
        self.__push_count += 1

    def sample(self, batch_size) -> List[Experience]:
        return random.sample(self.__memory, min(batch_size, len(self.__memory)))