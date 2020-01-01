import numpy as np
from PIL import ImageGrab
from PIL.Image import ANTIALIAS
from lib.console import Console
import random

class Environment:
    def __init__(self):
        self.__console = Console()
        self.__frameset_size = (64, 85, 4) 
        self.__frameset = None
        self.__last_actions = None
        self.__hot_encode_action_size = (4, 4)        

    @property
    def frameset_size(self):
        return self.__frameset_size

    @property
    def hot_encode_action_size(self):
        return self.__hot_encode_action_size     

    def hot_encode_action(self, action):
        # bit 1: JUMP 
        # bit 2: FIRE/ACC
        # bit 3: RIGHT
        # but 4: LEFT
        
        if action == 0: # RIGHT
            return np.array([0,0,1,0,])
        if action == 1: # RIGHT + FIRE
            return np.array([0,1,1,0,])            
        if action == 2: # RIGHT + JUMP
            return np.array([1,0,1,0,])                        
        if action == 3: # RIGHT + JUMP + FIRE
            return np.array([1,1,1,0,])              
        if action == 4: # LEFT
            return np.array([0,0,0,1,])           

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
        action = self.hot_encode_action(int(feedback[3]))

        # get screenshot as a [192,256,3] array with the last dimension representing RGB
        # this is the actual resolution of the game in the emulator
        # no need to do any extra processing
        img = ImageGrab.grabclipboard()
        # just a security because from time to time, img may be None...
        while img is None:
            img = ImageGrab.grabclipboard()

        img = img.convert('L')
        img = img.resize((85,64), resample=ANTIALIAS)

        # img.save(f'{random.random()}.png')

        # if self.__frameset is None:
        #     img_array = np.array(img)
        #     self.__frameset = np.stack([img_array, img_array, img_array, img_array])
        # else:
        #     last_screenshots = self.__frameset[1:,:,:]
        #     new_screenshot = np.array(img) 
        #     self.__frameset = np.insert(last_screenshots, 3, new_screenshot, axis=0)

        if self.__frameset is None:
            img_array = np.array(img)
            self.__frameset = np.stack([img_array, img_array, img_array, img_array], axis=2)
        else:
            img_array = np.array(img)
            self.__frameset = np.append(self.__frameset[:,:,1:], np.stack([img_array], axis=2), axis=2)

        if self.__last_actions is None:
            self.__last_actions = np.stack([action, action, action, action])
        else:
            actions = self.__last_actions[1:]
            self.__last_actions = np.insert(actions, 3, action, axis=0)            

        return(reward, self.__frameset, done, level_position, self.__last_actions)
