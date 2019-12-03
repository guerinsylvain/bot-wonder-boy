import keras
from keras.layers import Conv1D, Conv2D
from keras.layers.core import Dense, Flatten
from keras.models import Model, Sequential
from keras.optimizers import Adam

class Network:
    def __init__(self, image_size, n_out):
        self.__image_size = image_size
        self.__n_out = n_out
        self.__model = self.build_model()

    def build_model(self):           
        model = Sequential()
        model.add(Conv1D(16, kernel_size =(3), activation="relu", input_shape=self.__image_size))
        model.add(Conv1D(32, kernel_size =(3), activation="relu"))
        model.add(Conv1D(32, kernel_size =(3), activation="relu"))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))         
        model.add(Dense(self.__n_out, init="uniform", activation='relu'))         
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
        self.__model.fit(train_samples, train_labels, epochs=15, verbose=0)
    