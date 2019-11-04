import keras
from keras.layers import Conv2D
from keras.layers.core import Dense, Flatten
from keras.models import Model, Sequential
from keras.optimizers import Adam

class Network:
    def __init__(self, image_size, n_out):
        self.image_size = image_size
        self.model = self.build_model(image_size, n_out)

    def build_model(self, image_size, n_out):           
        model = Sequential()
        model.add(Conv2D(16, kernel_size =(3,3), activation="relu", input_shape=self.image_size))
        model.add(Conv2D(32, kernel_size =(3,3), activation="relu"))
        model.add(Conv2D(32, kernel_size =(3,3), activation="relu"))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))         
        model.add(Dense(n_out, init="uniform", activation='relu'))         
        model.compile(Adam(lr=.0001), loss='categorical_crossentropy', metrics=['accuracy'])
        print(model.summary())
        return model

    def compute(self, state):
        return self.model.predict(state)

    def train(self, train_samples, train_labels):
        self.model.fit(train_samples, train_labels, epochs=1, verbose=0)