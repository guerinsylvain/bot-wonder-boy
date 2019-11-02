from lib.experience import Experience
import random
from typing import List

class ReplayMemory:
    def __init__(self, capacity):
        self.memory = []
        self.push_count = 0
        self.capacity = capacity

    def write(self, initial_screenshot, action, reward, new_screenshot):
        experience = Experience(initial_screenshot, action, reward, new_screenshot)
        if len(self.memory) < self.capacity:
            self.memory.append(experience)
        else:
            self.memory[self.push_count % self.capacity] = experience
        self.push_count += 1

    def sample(self, batch_size) -> List[Experience]:
        return random.sample(self.memory, min(batch_size, len(self.memory)))