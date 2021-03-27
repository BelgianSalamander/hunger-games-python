from random import gauss,choice
from math import sqrt

from weapons import Weapon, Trap

accepted_deities = ['Ted the Dog','The Beaver', 'The Flying Spaghetti Monster', 'Satan', 'Uk\'otoa', 'Valar', 'Hashtag', 'Cthulhu', 'Wide Putin', 'The Random Green Thing', 'Harold the Giraffe']

class Player:
    def __init__(self,name,inventory = [], melee = 0.0, ranged = 0.0, intelligence = 0.0, stealth = 0.0, strength = 1.0,religion = None,hands = None):
        self.alive = True
        self.name = name
        self.inventory = inventory ##Items the player picked up
        if hands is None:
            self.weapons = [Weapon("hands",0.5,0,0.1,["{attacker} tried to slap {victim} but failed!"],["{attacker} slapped {victim} to death!"])]
        else:
            self.weapons = [hands]
        self.traps = []

        if religion is None:
            self.religion = choice(accepted_deities)
        else:
            self.religion = religion
        
        if melee:
            self.melee = melee
        else:
            self.melee = max(0,min(2,gauss(1,0.3))) ##Will be a multiplier for melee weapons/skills

        if ranged:
            self.ranged = ranged
        else:
            self.ranged = max(0,min(2,gauss(1,0.3))) ##Will be a multiplier for ranged weapons/skills

        if intelligence:
            self.intelligence = intelligence
        else:
            self.intelligence = max(0,min(2,gauss(1,0.3)))

        if stealth:
            self.stealth = stealth
        else:
            self.stealth = max(0.5,min(2,gauss(1,0.3)))
        self.strength = strength

    def attack(self):
        melee = 0
        ranged = 0
        intelligence = 0
        for w in self.weapons:
            melee += w.melee
            ranged += w.ranged
            intelligence += w.intelligence
        melee *=self.melee
        ranged *= self.ranged
        intelligence *= self.intelligence
        melee = sqrt(melee)
        ranged = sqrt(ranged)
        intelligence = sqrt(intelligence)
        return (melee+ranged+intelligence)*self.strength

    def add_weapon(self,weapon):
        if len(self.weapons) < 5:
            self.weapons.append(weapon)
        else:
            power = []
            for i in range(len(self.weapons)):
                if self.weapons[i].name == "hands":
                    power.append(-1)
                    continue
                melee = 0
                ranged = 0
                intelligence = 0
                for j in range(len(self.weapons)):
                    if i != j:
                        melee += self.weapons[j].melee
                        ranged += self.weapons[j].ranged
                        intelligence += self.weapons[j].intelligence
                    else:
                        melee += weapon.melee
                        ranged += weapon.ranged
                        intelligence += weapon.intelligence

                melee *= self.melee
                ranged *= self.ranged
                intelligence *= self.intelligence
                melee = sqrt(melee)
                ranged = sqrt(ranged)
                intelligence = sqrt(intelligence)
                power.append((melee+ranged+intelligence)*self.strength)
            minimum = max(power)
            if minimum > self.attack():
                ind = power.index(minimum)
                temp = self.weapons[ind]
                self.weapons[ind] = weapon
                print(f"{self.name} replaced their {temp.name} with a {weapon.name}")
            else:
                print("{:} couldn't pick up the {:} because they have too much weapons".format(self.name,weapon.name))
                
    def add_trap(self,trap):
        self.traps.append(trap)

    def __repr__(self):
        return f"{self.name} with {round(self.attack(),2)} attack damage of the {self.religion} religion"