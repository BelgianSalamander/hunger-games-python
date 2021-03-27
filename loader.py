import json
from player import Player

def load_people(hands = None):
    f = open('players.json','r')
    players = json.load(f)
    f.close()
    player_objects = []
    for name, data in players.items():
        player_objects.append(Player(name=name, **data, hands = hands))
    return player_objects