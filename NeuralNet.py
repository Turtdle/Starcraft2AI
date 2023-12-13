from tensorflow import keras
import tensorflow as tf

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

    def __init__(self):
        self.model = keras.Sequential([
            keras.layers.Dense(5, activation=tf.nn.relu),
            keras.layers.Dense(4, activation=tf.nn.relu),
            keras.layers.Dense(5, activation=tf.nn.relu),
            keras.layers.Dense(3, activation=tf.nn.softmax)

        ])
        self.model.compile(optimizer='adam', 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
        self.model.fit(self.inputs, self.outputs, epochs=5)

    def __init__(self, model):
        self.model = model
    
    def predict(self, inputs):
        return self.model.predict(inputs)
    

