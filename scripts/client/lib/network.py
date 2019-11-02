import keras
from keras.layers.core import Dense, Flatten
from keras.models import Model, Sequential
from keras.optimizers import Adam

class Network:
    def __init__(self, image_size, n_out):
        self.image_size = image_size
        self.model = self.build_model(image_size, n_out)

    def build_model(self, image_size, n_out):           
        vgg16_model = keras.applications.vgg16.VGG16(include_top=False, input_shape=self.image_size)
        model = Sequential()
        for layer in vgg16_model.layers: #[:-1]
            model.add(layer)
        for layer in model.layers:
            layer.trainable = False
        model.add(Flatten())
        model.add(Dense(n_out, activation='relu')) 
        # out = Dense(n_out, activation='relu')
        # model = Model(input=vgg16_model.input, output=out)        
        model.compile(Adam(lr=.0001), loss='categorical_crossentropy', metrics=['accuracy'])
        print(model.summary())
        return model

    def compute(self, state):
        return self.model.predict(state)

    def train(self, train_samples, train_labels):
        self.model.fit(train_samples, train_labels, validation_split=0.1, batch_size=10, epochs=1, shuffle=True, verbose=0)