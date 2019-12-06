import numpy as np
from PIL import ImageGrab
from PIL.Image import ANTIALIAS
from lib.console import Console
import random

class Environment:
    def __init__(self, gray_scale: bool):
        self.__console = Console()
        self.__frameset_size = (32, 32, 4) if gray_scale else (32, 32, 3, 4)
        self.__gray_scale = gray_scale
        self.__frameset = None

    @property
    def frameset_size(self):
        return self.__frameset_size

    def start(self):
        _ = self.__console.recv()

    def exit(self):
        self.__console.close()

    def sendAction(self, action):
        self.__console.send('{}\n'.format(action))

    def getState(self):
        buf = self.__console.recv()
        feedback = buf.split(' ')
        reward = int(feedback[0])
        done = int(feedback[1])
        level_position = int(feedback[2])

        # get screenshot as a [192,256,3] array with the last dimension representing RGB
        # this is the actual resolution of the game in the emulator
        # no need to do any extra processing
        img = ImageGrab.grabclipboard()
        # just a security because from time to time, img may be None...
        while img is None:
            img = ImageGrab.grabclipboard()

        if self.__gray_scale:
            img = img.convert('L')

        img = img.resize((32,32), resample=ANTIALIAS)

        # img.save(f'{random.random()}.png')

        screenshot = np.array(img) 

        if self.__frameset is None:
            self.__frameset = np.stack([img, img, img, img], axis=2)
        else:
            self.__frameset = np.append(self.__frameset[:,:,1:], np.stack([screenshot], axis=2), axis=2)

        return(reward, self.__frameset, done, level_position)
