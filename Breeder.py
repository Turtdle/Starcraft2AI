import NeuralNet
class Breeder:
    #the breeder class is used to breed two networks together
    def __init__(self, network1, network2):
        self.network1 = network1
        self.network2 = network2
        self.weights1 = network1.get_weights()
        self.weights2 = network2.get_weights()
        self.new_weights = []
        self.new_model = None
        self.breed()
        
    def breed(self):
        #breed the two networks together
        for i in range(len(self.weights1)):
            #for each layer
            layer1 = self.weights1[i]
            layer2 = self.weights2[i]
            new_layer = []
            for j in range(len(layer1)):
                #for each neuron
                neuron1 = layer1[j]
                neuron2 = layer2[j]
                new_neuron = []
                for k in range(len(neuron1)):
                    #for each weight
                    weight1 = neuron1[k]
                    weight2 = neuron2[k]
                    new_weight = (weight1 + weight2) / 2
                    new_neuron.append(new_weight)
                new_layer.append(new_neuron)
            self.new_weights.append(new_layer)
        self.new_model = NeuralNet(self.new_weights)
    
