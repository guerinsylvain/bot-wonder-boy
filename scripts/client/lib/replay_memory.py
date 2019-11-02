from lib.experience import Experience
import random
from typing import List

class ReplayMemory:
    def __init__(self):
        self.buffer = []
        self.length = 0
        self.max_length = 100000

    def write(self, initial_screenshot, action, reward, new_screenshot):
        if self.length >= self.max_length:
            self.buffer.pop(0)
            self.length -= 1
        experience = Experience(initial_screenshot, action, reward, new_screenshot)
        self.buffer.append(experience)
        self.length += 1

    def read(self, batch_size) -> List[Experience]:
        return random.sample(self.buffer, min(batch_size, self.length))