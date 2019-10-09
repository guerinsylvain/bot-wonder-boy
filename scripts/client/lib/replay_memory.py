import random

class ReplayMemory:
    def __init__(self):
        self.buffer = []
        self.length = 0
        self.max_length = 100000

    def write(self, data):
        if self.length >= self.max_length:
            self.buffer.pop(0)
            self.length -= 1
        self.buffer.append(data)
        self.length += 1

    def read(self, batch_size):
        return random.sample(self.buffer, min(batch_size, self.length))