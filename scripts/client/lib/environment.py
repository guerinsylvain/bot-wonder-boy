import numpy as np
from PIL import ImageGrab
from lib.console import Console

class Environment:    
    def __init__(self):
        self.console = Console()

    def start(self):
        _ = self.console.recv()

    def exit(self):
        self.console.close()

    def sendAction(self, action):
        self.console.send('{}\n'.format(action))

    def getState(self):
        buf = self.console.recv()
        feedback = buf.split(' ')    
        reward = int(feedback[0])
        done = int(feedback[1]) 
        # get screenshot as [192,256,3] array with the last dimension representing RGB
        screenshot = np.array(ImageGrab.grabclipboard()) 
        return(reward, screenshot, done)
