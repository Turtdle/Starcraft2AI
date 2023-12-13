from typing import Set

from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2.ids.ability_id import AbilityId
from sc2.unit import Unit
from sc2.data import Difficulty, Race
from sc2.units import Units
import numpy as np
import NeuralNet
from keras.models import load_model
class DoNothing(BotAI):
    async def on_step(self, iteration):
        pass


class MakeMoney(BotAI):
    """
    make base
    make worker
    make supply depot
    (auto saturate bases)
    """




    def __init__(self, net : NeuralNet):
        super().__init__()
        self.placeholders: Set[Unit] = set()
        self.net : NeuralNet = net
        self.reward= {
            "money": 0,
            "supply": 0,
            "supply_blocked": 0,
            "income_rate": 0,
            "invalid action": 0
        }
        self.money = []

    async def on_start(self):
        self.client.game_step = 50
        await self.client.debug_show_map()

    async def build_supply_depot(self):
        if self.can_afford(UnitTypeId.SUPPLYDEPOT) and self.already_pending(UnitTypeId.SUPPLYDEPOT) < 2:
            await self.build(UnitTypeId.SUPPLYDEPOT, near=self.townhalls.first)
        else:
            self.reward["invalid action"] += 1
            return
        
    async def build_worker(self):
        try:
            townhall = None
            for th in self.townhalls:
                if th.is_idle:
                    townhall = th
                    break
                if townhall == None or townhall.train_progress > th.train_progress:
                    townhall = th
            if townhall == None:
                self.reward["invalid action"] += 1
                return

            if self.can_afford(UnitTypeId.SCV):
                townhall.train(UnitTypeId.SCV)
            else:
                self.reward["invalid action"] += 1
                return
        except AttributeError as e:
            print(str(e))
            return
    
    async def build_base(self):
        if self.can_afford(UnitTypeId.COMMANDCENTER):
            await self.expand_now()
        else:
            self.reward["invalid action"] += 1
            return

    async def sature_base(self):
        await self.distribute_workers()

    async def return_idle_workers(self):
        if self.townhalls:
            for w in self.workers.idle:
                th: Unit = self.townhalls.closest_to(w)
                mfs: Units = self.mineral_field.closer_than(10, th)
                if mfs:
                    mf: Unit = mfs.closest_to(w)
                    w.gather(mf)
        
    async def lower_all_depots(self):
        for depot in self.structures(UnitTypeId.SUPPLYDEPOT).ready:
            depot(AbilityId.MORPH_SUPPLYDEPOT_LOWER)

    async def on_step(self, iteration):
        
        left_game = False
        if not left_game:
            prediction = self.net.predict(self.get_inputs())
            #get the highest prediction
            """
            1 make base
            2 make worker
            3 make supply depot
            """
            print(prediction.argmax())
            action = prediction.argmax()
            if action == 2:
                await self.build_base()
            elif action == 0:
                await self.build_worker()
            elif action == 1:
                await self.build_supply_depot()
            else:
                self.reward["invalid action"] += 1
                return
            
            self.reward["money"] = self.minerals
            self.reward["supply"] = self.supply_used
            self.reward["income_rate"] = self.calculate_income()
            self.money.append(self.minerals)
            await self.return_idle_workers()
            await self.lower_all_depots()
            await self.sature_base()
                    #if supply capped
            if self.supply_left <= 0:
                #increment supply blocked in reward
                self.reward["supply_blocked"] += 1
            try:
                if self.time >= 4 * 60:
                    if(self.client is not None):
                        await self.client.leave()
                        left_game = True
            except:
                print("game ended so command failed")

    def get_inputs(self):
        inputs = np.array([self.time, self.workers.amount, self.supply_used, self.supply_cap, self.minerals])
        inputs = inputs.reshape((1, 5))
        return inputs

    def calculate_income(self):
        bases = self.townhalls.amount
        workers = self.workers.amount
        if workers / 16 > bases:
            return bases
        else:
            return workers / 16

def run_bot(id : int):
    net = NeuralNet.NeuralNet()
    AI = MakeMoney(net)
    run_game(
        maps.get("AcropolisLE"),
        [Bot(Race.Terran, AI), Bot(Race.Terran, DoNothing())],
        realtime=False,
        save_replay_as="MakeMoney.SC2Replay",
    )
    reward = AI.reward
    AI.net.save("MakeMoney" + str(id) + ".h5")
    with open("MakeMoney" + str(id) + ".txt", "w") as f:
        f.write(str(reward))

def run_bot_from_file(Filename : str, id : int):
    #loads neural net from file
    model1 = load_model(Filename)
    net = NeuralNet.NeuralNet(model=model1)
    AI = MakeMoney(net)
    run_game(
        maps.get("AcropolisLE"),
        [Bot(Race.Terran, AI), Bot(Race.Terran, DoNothing())],
        realtime=False,
        save_replay_as="MakeMoney.SC2Replay",
    )
    
    #after game is over, calculate reward
    reward = AI.reward
    #save neural net
    AI.net.save("MakeMoney" + str(id))
    #save reward
    with open("saves/MakeMoney" + str(id) + ".txt", "w") as f:
        f.write(str(reward))