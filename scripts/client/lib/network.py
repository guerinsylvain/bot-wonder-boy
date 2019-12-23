import keras
from keras.layers import Conv2D
from keras.layers.core import Dense, Flatten
from keras.models import Model, Sequential, load_model
from keras.optimizers import Adam
from keras.layers import LeakyReLU

class Network:
    def __init__(self, frameset_size, n_out, batch_size):
        self.__frameset_size = frameset_size
        self.__n_out = n_out
        self.__model = self.build_model()
        self.__batch_size = batch_size

    def build_model(self):           
        model = Sequential()
        model.add(Conv2D(32, kernel_size =(3,3), padding='same', input_shape=self.__frameset_size))     
        model.add(LeakyReLU(alpha=0.2))
        model.add(Conv2D(64, kernel_size =(3,3), padding='same' ))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Conv2D(128, kernel_size =(3,3), padding='same'))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Flatten())
        model.add(Dense(256))     
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

    def load_model(self, fileName):
        self.__model = load_model(fileName)
    
    def save_model(self, fileName):
        self.__model.save(fileName)

    def train(self, train_samples, train_labels):
        return self.__model.fit(train_samples, train_labels, epochs=5, verbose=0, batch_size=self.__batch_size)
    