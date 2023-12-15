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

def get_best_network(start,finish):
    rewards = {}
    for j in range(start, finish+1):

        for i in range(1, 100):
            with open("saves" + str(j) + "/MakeMoney" + str(i) + ".txt", "r") as f:
                reward = eval(f.read())
                rewards["saves" + str(j) + "/MakeMoney" + str(i) + ".txt"] = calculate_reward(reward)
    #returns the best key and value
    return max(rewards, key=rewards.get), rewards[max(rewards, key=rewards.get)]

def main():
    #get average rewards of epoch 2-11
    #get best of each epoch, print results, cut the decimal to 2 places
    for i in range(2, 12):
        rewards = get_rewards(str(i))
        scores = [calculate_reward(reward) for reward in rewards]
        average = sum(scores) / len(scores)
        average = round(average, 2)
        print("Epoch " + str(i) + " average: " + str(average))
        best = max(scores)
        best = round(best, 2)
        print("Epoch " + str(i) + " best: " + str(best))
    print ("Best network: " + str(get_best_network(2, 11)))
        

if __name__ == "__main__":
    main()