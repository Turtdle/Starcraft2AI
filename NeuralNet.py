from tensorflow import keras
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
class NeuralNet:
    """
    nn has inputs: 
    
    game time
    worker count
    supply count
    supply max
    current money

    """

    """
    nn has outputs:

    make base
    make worker
    make supply depot
    
    """

    def __init__(self, model = None):
        if model != None:
            self.model = model
        else:
            self.model = tf.keras.Sequential()
            # Add the input layer with 5 nodes
            self.model.add(Dense(64, input_shape=(5,), activation='relu'))

            # Add the first hidden layer with 128 nodes
            self.model.add(Dense(128, activation='relu'))

            # Add the second hidden layer with 64 nodes
            self.model.add(Dense(64, activation='relu'))

            # Add the output layer with 3 nodes (since you have 3 outputs)
            self.model.add(Dense(3, activation='softmax'))
            self.model.compile(optimizer='adam', 
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

    
    def predict(self, inputs):
        return self.model.predict(inputs)
    
    def save(self, save_name):
        self.model.save(save_name)
    
    def load(save_name):
        return NeuralNet(keras.models.load_model(save_name))
    

