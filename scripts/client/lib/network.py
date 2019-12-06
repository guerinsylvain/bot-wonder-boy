import keras
from keras.layers import Conv1D, Conv2D
from keras.layers.core import Dense, Flatten
from keras.models import Model, Sequential
from keras.optimizers import Adam
from keras.layers import LeakyReLU

class Network:
    def __init__(self, frameset_size, n_out):
        self.__frameset_size = frameset_size
        self.__n_out = n_out
        self.__model = self.build_model()

    def build_model(self):           
        model = Sequential()
        model.add(Conv2D(32, kernel_size =(3,3), input_shape=self.__frameset_size))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Conv2D(64, kernel_size =(5,5), strides=2))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Conv2D(64, kernel_size =(5,4), strides=4))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Flatten())
        model.add(Dense(128))     
        model.add(LeakyReLU(alpha=0.2))    
        model.add(Dense(self.__n_out, init="uniform"))         
        model.add(LeakyReLU(alpha=0.2))
        model.compile(Adam(lr=.0001), loss='mse', metrics=['accuracy'])
        print(model.summary())
        return model

    @property
    def weights(self):
        return self.__model.get_weights()

    @weights.setter
    def weights(self, weights):
        self.__model.set_weights(weights)

    def compute(self, state):
        return self.__model.predict(state)

    def load_weights(self, fileName):
        self.__model.load_weights(f'{fileName}.h5')
    
    def save_weights(self, fileName):
        self.__model.save_weights(f'{fileName}.h5')

    def train(self, train_samples, train_labels):
        return self.__model.fit(train_samples, train_labels, epochs=15, verbose=0)
    