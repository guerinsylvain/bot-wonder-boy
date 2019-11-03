import numpy as np
from PIL import ImageGrab
from lib.console import Console

class Environment:    
    def __init__(self):
        self.console = Console()
        self.image_size =  (192, 256, 3)

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
        # get screenshot as a [192,256,3] array with the last dimension representing RGB
        # this is the actual resolution of the game in the emulator
        # no need to do any extra processing
        img = ImageGrab.grabclipboard()
        # just a security because from time to time, img may be None...
        while img is None:
            img = ImageGrab.grabclipboard()
        
        screenshot = np.array(img) 
        return(reward, screenshot, done)
