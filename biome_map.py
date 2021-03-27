from random import randint, choice, gauss
from guaranteed_execution import execute, tester

class BiomeMap:
    def __init__(self):
        self.biomes = []

class Biome:
    def __init__(self,
                name,
                temperature,
                humidity,
                altitude,
                weirdness,
                offset):

        self.name = name
        self.values = (temperature, humidity, altitude, weirdness)
        self.offset = offset

    def player_action(self, player):
        pass

    def group_action(self, group):
        pass

class Forest(Biome):
    def __init__(self):
        super().__init__(0.2, 0.3,-0.5,-0.7,0.0)

        self.forest_percent = randint(70,100)





