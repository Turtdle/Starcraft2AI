import Bot
import os
from rl import DQNAgent
from rl.agents import DQNAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory
import NeuralNet
import numpy as np
ID = 470925


def calculate_reward(reward):
    #{'money': 3120, 'supply': 15, 'supply_blocked': 98, 'income_rate': 0.9375, 'invalid action': 104}
    """
    money is worth 1 point per 1000 minerals
    supply is worth 1 point per supply
    supply blocked is worth -1 point per supply blocked
    income rate is worth 100 points per income rate
    invalid action is worth -1 points per 20 invalid action
    """
    a = []
    a.append(reward["money"] / 1000)
    a.append(reward["supply"]*2)
    a.append(-reward["supply_blocked"])
    a.append(-reward["invalid action"] / 20)
    a.append(reward["income_rate"] * 100)
    return a
    #return reward["money"] / 1000 + reward["supply"]*2 - reward["supply_blocked"] - reward["invalid action"] / 20 + reward["income_rate"] * 100

def test_network():
    if not os.path.exists(str(ID) + ".h5"):
        Bot.run_bot(ID)
    else:
        Bot.run_bot_from_file(str(ID) + ".h5", ID)

def evaluate_network():
    if not os.path.exists(str(ID) + ".txt"):
        return None
    with open(str(ID) + ".txt", "r") as f:
        reward = eval(f.read())
    return calculate_reward(reward)

def get_network():
    if not os.path.exists(str(ID) + ".h5"):
        return None
    return NeuralNet.load(str(ID) + ".h5")

def train():
    network = get_network()
    #if the network builds a worker but is supply blocked, it will be penalized
    #if the network builds a supply depot but is 8 or more below the supply cap, it will be penalized
    #if the network builds a base but has than base count / (workers/12) > 1, it will be penalized
    #if the network builds a worker it will be rewarded
    #if the network builds a supply depot it will be rewarded
    #if the network builds a base it will be rewarded
    """
    game time
    worker count
    supply count
    supply max
    current money
    """
    for i in range(110):
        #game time = i
        #worker count = 12
        #supply count = 12
        #supply max = 15
        #current money = 0
        #money goes up by 5 per worker every 5 Is
        #supply goes up by 1 when the model makes a worker
        #supply goes up by 8 when the model makes a supply depot
        #can only make a worker if supply is not capped
        #can only make a base if you have 400 minerals
        game_time = i
        worker_count = 12
        supply_count = 12
        supply_max = 15
        current_money = 0
        inputs = np.array([game_time, worker_count, supply_count, supply_max, current_money])
        inputs = inputs.reshape((1, 5))
        c = network.predict(inputs)
        c = c[0]


    