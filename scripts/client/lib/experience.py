class Experience:
    def __init__(self, start_state, action, reward, end_state, done):
        self.start_state = start_state
        self.action = action
        self.reward = reward
        self.end_state = end_state
        self.done = done