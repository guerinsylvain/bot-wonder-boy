from tensorflow.keras.layers import AveragePooling2D, Conv2D, Concatenate, Dense, Flatten
from tensorflow.keras.models import Model, Sequential, load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.applications.inception_v3 import InceptionV3

class Network:
    def __init__(self, frameset_size, n_out, last_actions_size):
        self.__frameset_size = frameset_size
        self.__n_out = n_out
        self.__last_actions_size = last_actions_size
        self.__model = self.build_model()

    def build_actions_model(self):
        model = Sequential(name='last_actions')
        model.add(Dense(32, input_shape=(self.__last_actions_size)))     
        model.add(LeakyReLU(alpha=0.5)) 
        model.add(Flatten())
        return model

    def build_movements_model(self):
        # model = Sequential(name='frameset')
        # model.add(Conv2D(32, kernel_size =(3,3), input_shape=self.__frameset_size))     
        # model.add(LeakyReLU(alpha=0.2))
        # model.add(Conv2D(64, kernel_size =(3,3)))
        # model.add(LeakyReLU(alpha=0.2))
        # model.add(Conv2D(128, kernel_size =(3,3), strides = 2))
        # model.add(LeakyReLU(alpha=0.2))
        # model.add(AveragePooling2D(pool_size=2))               
        # model.add(Flatten())
        pre_trained_model = InceptionV3(input_shape = self.__frameset_size, 
                                        include_top = False, # Leave out the last fully connected layer
                                        weights = 'imagenet')

        for layer in pre_trained_model.layers:
            layer.trainable = False
  
        x = Flatten()(pre_trained_model.layers[-1].output)
        model = Model(pre_trained_model.layers[0].input, x)

        print(model.summary())
        return model        

    def build_model(self):           
        actions_model = self.build_actions_model()
        movement_model = self.build_movements_model()
        
        combinedInput = Concatenate()([actions_model.output, movement_model.output])
        x = Dense(256)(combinedInput)
        x = LeakyReLU(alpha=0.2)(x)
        x = Dense(self.__n_out, kernel_initializer="uniform")(x)
        x = LeakyReLU(alpha=0.2)(x)
        model = Model(inputs = [actions_model.input, movement_model.input], outputs = x)

        model.compile(Adam(lr=.0001), loss='mae', metrics=['accuracy'])
        print(model.summary())
        return model

    @property
    def weights(self):
        return self.__model.get_weights()

    @weights.setter
    def weights(self, weights):
        self.__model.set_weights(weights)

    def compute(self, state, batch_size):
        return self.__model.predict(state, batch_size = batch_size)

    def load_model(self, fileName):
        self.__model = load_model(fileName)
    
    def save_model(self, fileName):
        self.__model.save(fileName)

    def train(self, train_samples, train_labels, num_epochs, batch_size):
        return self.__model.fit(train_samples, train_labels, epochs=num_epochs, verbose=0, batch_size=batch_size)
    