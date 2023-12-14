from NeuralNet import NeuralNet
import random
from tensorflow.keras.models import Sequential

import numpy as np

def breed(model1 : NeuralNet, model2 : NeuralNet):
    new_model = Sequential()

    for layer1, layer2 in zip(model1.model.layers, model2.model.layers):
        use_layer1 = np.random.choice([True, False])
        new_model.add(layer1 if use_layer1 else layer2)
    new_model.compile(optimizer='adam', 
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
    return NeuralNet(new_model)

def mutate(neural : NeuralNet, mutation_rate=0.05):
    mutated_model = Sequential()
    for layer in neural.model.layers:
        new_layer = layer.__class__.from_config(layer.get_config())
        new_layer.build(layer.input_shape)
        if np.random.rand() < mutation_rate and new_layer.count_params() > 0 :
            new_weights = [np.random.standard_normal(w.shape) for w in layer.get_weights()]
            new_layer.set_weights(new_weights)

        mutated_model.add(new_layer)
    mutated_model.compile(optimizer='adam', 
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
    return NeuralNet(mutated_model)

    
def get_networks(epoch):
    networks = []
    for i in range(0, 100):
        networks.append(NeuralNet.load("saves" + epoch + "/MakeMoney" + str(i) + ".h5"))
    return networks

def get_rewards(epoch):
    rewards = []
    for i in range(1, 100):
        with open("saves" + epoch + "/MakeMoney" + str(i) + ".txt", "r") as f:
            reward = eval(f.read())
            rewards.append(reward)
    return rewards

def calculate_reward(reward):
    #{'money': 3120, 'supply': 15, 'supply_blocked': 98, 'income_rate': 0.9375, 'invalid action': 104}
    """
    money is worth 1 point per 1000 minerals
    supply is worth 1 point per supply
    supply blocked is worth -1 point per supply blocked
    income rate is worth 100 points per income rate
    invalid action is worth -1 points per 20 invalid action
    """
    return reward["money"] / 1000 + reward["supply"] - reward["supply_blocked"]/2 - reward["invalid action"] / 20 + reward["income_rate"] * 100

    

def get_best_networks(epoch):
    networks = get_networks(epoch)
    rewards = get_rewards(epoch)

    if not networks or not rewards:
        print("Error: No networks or rewards found.")
        return None
    scores = [calculate_reward(reward) for reward in rewards]
    network_scores = list(zip(networks, scores))

    sorted_network_scores = sorted(network_scores, key=lambda x: x[1], reverse=True)

    # Extract the top-performing networks
    top_networks = [network for network, score in sorted_network_scores[:40]] 

    return top_networks

def breed_networks(epoch):
    networks = get_networks(epoch)
    best_networks = get_best_networks(epoch)
    #breed 40 networks from the top 40 networks
    #breed the rest 60 by choosing one of the top 40 and one randomly
    new_networks = []
    for i in range(40):
        if i == 39:
            new_networks.append(breed(best_networks[i], best_networks[0]))
        else:
            new_networks.append(breed(best_networks[i], best_networks[i + 1]))
    for i in range(60):
        new_networks.append(breed(random.choice(best_networks), random.choice(networks)))
    #mutate lower 80 networks
    for i in range(80):
        new_networks[i+20] = mutate(new_networks[i+20])
    #save all networks
    for i in range(100):
        new_networks[i].save("saves" + str(int(epoch)+1) + "/MakeMoney" + str(i) + ".h5")


def main():
    breed_networks('3')

if __name__ == "__main__":
    main()
