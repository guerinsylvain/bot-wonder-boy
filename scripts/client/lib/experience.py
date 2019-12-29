class Experience:
    def __init__(self, intial_frameset, initial_last_actions, action, reward, new_frameset, new_last_actions, done):
        self.intial_frameset = intial_frameset
        self.initial_last_actions = initial_last_actions
        self.action = action
        self.reward = reward
        self.new_frameset = new_frameset
        self.new_last_actions = new_last_actions
        self.done = done