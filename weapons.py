from random import random

class Weapon:
    def __init__(self,name,melee,ranged,intelligence,miss,hit):
        self.name = name
        self.melee = melee
        self.ranged = ranged
        self.intelligence = intelligence
        self.miss = miss
        self.hit = hit

class Trap:
    def __init__(self,name,owner,prob,strength_decrease_min,strength_decrease_max,kill,fail,setup):
        self.name = name
        self.owner = owner
        self.prob = prob
        self.strength_decrease = random()*(strength_decrease_max-strength_decrease_min)+strength_decrease_min
        self.kill = kill
        self.fail = fail
        self.setup = setup