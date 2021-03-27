from random import randint, choice, gauss, shuffle, random, seed
import numpy as np
from math import *

from weapons import Weapon, Trap
from names import name
from formatting import represent, repr_players
from player import Player
from loader import load_people
from guaranteed_execution import tester, execute, GameEnded

import sys
import json

output = open('output.txt','w')
sys.stdout = output

s = hash(str(random()**2)+str(random()))
print('Seed:',s)
seed(s)

file = open('weapons/hand.json','r')
hand = json.load(file)
attr = (hand['name'], hand['melee'], hand['ranged'], hand['intelligence'], hand['misses'], hand['kills'])

file = open("weapons/weapons.json","r")
weapons = json.load(file)
file.close()
##weapons = weapons.split("\n\n")
##weapons = [(n.split("\n")[1].replace("\t","").split(","),[float(a) for a in n.split("\n")[2].replace("\t","").split(",")],n.split("\n")[3].replace("\t","").split("|")) for n in weapons]
##weapons = [(int(n[1][0]),(n[0],n[1][1:],n[2])) for n in weapons]
##temp = []
##for a in weapons:
##    for i in range(a[0]):
##        temp.append(a[1])
##weapons = temp


file = open("traps.txt","r")
traps = file.read()
file.close()
traps = traps.split("\n\n")
#print(traps)
#print("\n")
traps = [(n.split("\n")[1].replace("\t","").split(","),[float(a) for a in n.split("\n")[2].replace("\t","").split(",")],n.split("\n")[3].replace("\t","").split("|"),n.split("\n")[4].replace("\t","").split("|"),n.split("\n")[5].replace("\t","").split("|")) for n in traps]
traps = [(int(n[1][0]),(n[0],n[1][1:],n[2],n[3],n[4])) for n in traps]
temp = []
for a in traps:
    for i in range(a[0]):
        temp.append(a[1])
traps = temp
#print(traps)


sword = ["sliced","stabbed","impaled","killed","defeated","murdered","decapitated","beheaded","tortured","suprised"]
dagger = ["assassinated","stabbed"]
explode = ["dismembered","blown up","exploded","yeeted"]
yummy = ["very nourishing", "delicious", "amazing", "rejuvenating", "yum"]
body = ["right leg","left leg","clavicle","hip","ankles","nose","collar bone","neck","wrist","hands","finger"]
vital_body_parts = ["heart", "head", "stomach", "liver"]
triggered = ["set off","triggered","fallen into"]
foods = ['some roots', 'some frog legs', 'some leaves', 'some grass', 'a fish', 'a weird bird']
good_foods = ['two loaves of bread','a gluten free muffin', 'jelly beans', 'vegan cookies', 'beef jerkey', 'a protein milkshake', 'a suspicious green blob', 'a fish fillet', 'some crackers']

accepted_deities = ['Ted the Dog','The Beaver', 'The Flying Spaghetti Monster', 'Satan', 'Uk\'otoa', 'Valar', 'Hashtag', 'Cthulhu', 'Wide Putin', 'The Random Green Thing', 'Harold the Giraffe']

animal_killings = ['defeated','murdered','eaten','squashed','surprised','beheaded','mauled','dismembered']
animal_adjectives = ['diseased','giant','miniature','hungry','enraged','yellow','dead','poisonous']
animals = ['orangutan','crocodile','chicken','alpaca','duck','cat','elephant','fish','horse','rat','eel','pelican']

get = ['acquired', 'got', 'found', 'grabbed']

random_deaths = ['{player.name} had a heart attack!',
    '{player.name} starved to death. LOL!',
    '{player.name} was crushed by a falling tree!',
    '{player.name} ate a raw frog and died!',
    '{player.name} rolled down a hill and died of internal bleeding',
    '{player.name} climbed a mountain for a better viewpoint. They froze to death. What a loser!',
    '{player.name} tripped on a stick. They fell over and bumped their head. They fell into a coma and were later killed by a {choice(animal_adjectives)} {choice(animals)}',
    '{player.name} tried to escape the arena. They fell off because the world is flat',
    '{player.name} tripped on a rock and was killed by a random sword which just happened to be there!'
    ]

def exclusive_choice(l,exclusions):
    n = randint(0,len(l)-1-len(exclusions))
    while l[n] in exclusions:
        n += 1
    return l[n]

daytime = ['{player.name} walked around and saw a {choice(animals)}!',
    '{player.name} slipped in mud!',
    '{player.name} wondered about the meaning of life',
    '{player.name} contemplated suicide',
    '{player.name} was having day dreams about {exclusive_choice(self.players, [player]).name}',
    '{player.name} worshipped {player.religion}']

class Loop(Exception):
    pass



class Game:
    def __init__(self):
        self.players = []
        self.alive_players = []
        self.kills = {}
        self.active_traps = []
        terrain = [(self.lake,2),(self.desert,4)]

    @tester
    def cornucopia(self):
        if randint(1,3) == 1:
            print(f"Weapons and traps have been added to the cornucopia!")
            groups = [group for group in self.groups if randint(1,3) != 1]
            if len(groups) == 0:
                groups.append(choice(self.groups))
            players = []
            for group in groups:
                players = players + group

            print(f"{repr_players(players)} have decided to go!")
            for i in range(max(3,int(gauss(len(players),0.5)))):
                if randint(1,3) <= 2 or len(groups) == 1:
                    player = choice(players)
                    total = 0
                    for weapon in weapons:
                        total += weapon['weight']

                    val = random()*total

                    for weapon in weapons:
                        val -= weapon['weight']
                        if val <= 0:
                            break

                    name = choice(weapon['names'])
                    print(f'{player.name} found a {name}!')   
                    player.add_weapon(Weapon(name,weapon['melee'],weapon['ranged'],weapon['intelligence'],weapon['misses'],weapon['kills']))
                else:
                    group1 = choice(groups)
                    group2 = exclusive_choice(groups,[group1])
                    self.group_fight(group1,group2,0,[players])
                    if len(group1) == 0:
                        del self.groups[self.groups.index(group1)]
                        del groups[groups.index(group1)]
                    elif len(group2) == 0:
                        del self.groups[self.groups.index(group2)]
                        del groups[groups.index(group2)]

        elif randint(1,2) == 2:
            print('Food has been added to the cornucopia!')
            groups = [group for group in self.groups if randint(1,3) != 1]
            if len(groups) == 0:
                groups.append(choice(self.groups))
            players = []
            for group in groups:
                players = players + group

            print(f"{repr_players(players)} have decided to go!")
            for i in range(max(2,int(gauss(len(players)*0.6,0.5)))):
                if randint(1,4) != 1:
                    player = choice(players)
                    print(f'{player.name} {choice(get)} {choice(good_foods)}')
                    player.strength *= (1+random()*0.6)
                else:
                    try:
                        player1 = choice(players)
                        player2 = exclusive_choice(players, [group for group in self.groups if player1 in group][0])
                        strength1 = player1.attack()
                        strength2 = player2.attack()
                        pronoun, possesive = 'them', 'their'
                        n = random()*(1+strength1+strength2)
                        if n < strength1:
                            attack, victimise = player1, player2
                        elif n < strength2:
                            attack, victimise = player2, player1
                        
                        if n < strength2:
                            attacker,victim = attack.name, victimise.name
                            weapon = choice(attack.weapons)
                            name = weapon.name
                            print(eval('f"'+choice(weapon.hit)+'"'))
                            del self.alive_players[self.alive_players.index(victimise)]
                            del players[players.index(victimise)]
                            group = [group for group in self.groups if victimise in group][0]
                            del group[group.index(victimise)]
                            if len(group) == 0:
                                del self.groups[self.groups.index(group)]
                        else:
                            attacker,victim = player1.name,player2.name
                            print(eval("f'"+ choice(choice(player1.weapons).miss)+"'"))
                    except:
                        pass
    
    def purge_wacky_groups(self):
        for i in range(len(self.groups) - 1, -1, -1):
            if len(self.groups[i]) == 0:
                del self.groups[i]
                continue
            for j in range(len(self.groups[i])-1, -1, -1):
                if self.groups[i][j] not in self.alive_players:
                    del self.groups[i][j]

        if len(self.alive_players) == 1:
            raise GameEnded

    @tester
    def animal_attack(self):
        if randint(1,8) == 1:
            player = choice(self.alive_players)
            adjective = choice(animal_adjectives)
            if randint(1,2):
                n = randint(0,len(animal_adjectives)-2)
                if animal_adjectives[n] == adjective:
                    n += 1
                adjective = adjective + ' ' + animal_adjectives[n]
            if random()*3 >player.attack():
                print(f'{player.name} was {choice(animal_killings)} by a {adjective} {choice(animals)}!')
                group = [group for group in self.groups if player in group][0]
                del group[group.index(player)]
                if len(group) == 0:
                    del self.groups[self.groups.index(group)]
                del self.alive_players[self.alive_players.index(player)]
            else:
                print(f'{player.name} was almost {choice(animal_killings)} by a {adjective} {choice(animals)} but it failed and died!')
    
    @tester
    def invite(self):
        if len(self.alive_players) <= 3:
                raise Loop
        groups_of_one = [group for group in self.groups if len(group) == 1]
        group = choice(groups_of_one)
        player = group[0]
        del self.groups[self.groups.index(group)]
        group = choice(self.groups)
        print(f'{repr_players(group)} invited {player.name} to join their gang!')
        group.append(player)

    @tester
    def combat(self): ##Does combat between two groups
        group1 = choice(self.groups) ##Chooses random group to start combat
        total = sum([player.stealth for player in self.alive_players if player not in group1]) ##Gets total stealth of all players
        n = random() * total
        index = 0
        while sum(player.stealth for player in self.alive_players[:index + 1]) < n: ##Selects a random team based on total stealth
            index += 1
        if self.groups[index] == group1:
            index += 1
        group2 = self.groups[index] ##Select group two and make sure it is not the same as group one
        self.group_fight(group1,group2) ##Do group fight
        if len(group1) == 0: ##Delete groups if empty
            del self.groups[self.groups.index(group1)]
        elif len(group2) == 0:
            del self.groups[index]

    @tester
    def random_death(self):
        player = choice(self.alive_players)
        print(eval("f'" + choice(random_deaths) + "'"))
        del self.alive_players[self.alive_players.index(player)]
        group = [group for group in self.groups if player in group][0]
        del group[group.index(player)]
        if len(group) == 0:
            del self.groups[self.groups.index(group)]

    @tester
    def religion_argument(self):
        G = [group for group in self.groups if len(group) > 1]
        group = choice(G)
        religions = list(set([player.religion for player in group]))
        if len(religions) == 1:
            print(f'{repr_players(group)} discuss the supremacy of {religions[0]}')

        else:
            religion_1 = religions[:len(religions)//2]
            religion_2 = religions[len(religions)//2:]
            group1 = [player for player in group if player.religion in religion_1]
            group2 = [player for player in group if player.religion in religion_2]
            del self.groups[self.groups.index(group)]
            self.groups.append(group1)
            self.groups.append(group2)
            print(f'{repr_players(group1)} argued with {repr_players(group2)} about the influence of {choice(religions)}')
            self.group_fight(group1,group2)
            if len(group1) == 0:
                del self.groups[self.groups.index(group1)]
                        
            if len(group2) == 0:
                del self.groups[self.groups.index(group2)]

    @tester
    def daytime_activity(self):
        player = choice(self.alive_players)
        print(eval("f'"+choice(daytime)+"'"))

    @tester
    def cook_food(self):
        group = choice(self.groups)
        food = choice(foods)
        print(f"{repr_players(group)} started a fire to cook {food}!")

        if randint(1,3) == 1:
            n = randint(0,len(self.groups)-2)
            if self.groups[n] == group:
                n += 1
            other_group = self.groups[n]
            print(f"{repr_players(other_group)} saw the fire and went to attack them")
            if randint(1,2) == 1:
                print(f"{repr_players(group)} {'were' if len(group) > 1 else 'was'} caught by surprise!")
                self.group_fight(other_group,group,1)
            else:
                if randint(1,3) == 1:
                    print(f"{repr_players(group)} heard {repr_players(other_group)} coming and ran away")
                    return
                else:
                    print(f"{repr_players(group)} heard {repr_players(other_group)} coming but it was too late!")
                    self.group_fight(other_group,group,0)
            if len(group) > 0 and len(other_group) > 0:
                if randint(1,2) == 1:
                    print(f"{repr_players(other_group)} ran away!")
                    if randint(1,3) <= 2:
                        print(f"{repr_players(group)} ate the {' '.join(food.split(' ')[1:])}. It was {choice(yummy)}!")
                        for member in group:
                            member.strength *= 1.2
                    else:
                        toxicity = random()
                        print(f"{repr_players(group)} ate the {' '.join(food.split(' ')[1:])}. It was uncooked!")
                        for player in group:
                            n = random()
                            if n < toxicity/3:
                                print(f"{player.name} dies of food poisoning!")
                                del self.alive_players[self.alive_players.index(player)]
                                del group[group.index(player)]
                            elif n < toxicity:
                                print(f"{player.name} is weakened from food poisoning")
                                player.strength *= (1-toxicity/4-random()/15)
                        if len(group) == 0:
                            del self.groups[self.groups.index(group)]

                else:
                    print(f"{repr_players(group)} ran away!")
                    if randint(1,2) <= 1:
                        print(f"{repr_players(other_group)} ate the {' '.join(food.split(' ')[1:])}. It was {choice(yummy)}!")
                        for member in group:
                            member.strength *= 1.2
                    else:
                        toxicity = random()
                        print(f"{repr_players(other_group)} ate the {' '.join(food.split(' ')[1:])}. It was uncooked!")
                        for player in other_group:
                            n = random()
                            if n < toxicity/3:
                                print(f"{player.name} dies of food poisoning!")
                                del self.alive_players[self.alive_players.index(player)]
                                del other_group[other_group.index(player)]
                            elif n < toxicity:
                                print(f"{player.name} is weakened from food poisoning")
                                player.strength *= (1-toxicity/4-random()/15)
                        if len(other_group) == 0:
                            del self.groups[self.groups.index(other_group)]

            elif len(group) == 0 and len(other_group) > 0:
                if randint(1,3) <= 2:
                    print(f"{repr_players(other_group)} ate the {' '.join(food.split(' ')[1:])}. It was {choice(yummy)}!")
                    for member in group:
                        member.strength *= 1.2
                else:
                    toxicity = random()
                    print(f"{repr_players(other_group)} ate the {' '.join(food.split(' ')[1:])}. It was uncooked!")
                    for player in other_group:
                        n = random()
                        if n < toxicity/3:
                            print(f"{player.name} dies of food poisoning!")
                            del self.alive_players[self.alive_players.index(player)]
                            other_group[other_group.index(player)]
                        elif n < toxicity:
                            print(f"{player.name} is weakened from food poisoning")
                            player.strength *= (1-toxicity/4-random()/15)
                    if len(other_group) == 0:
                        del self.groups[self.groups.index(other_group)]
                del self.groups[self.groups.index(group)]

            elif len(group) > 0 and len(other_group) == 0:
                if randint(1,3) <= 2:
                    print(f"{repr_players(group)} ate the {' '.join(food.split(' ')[1:])}. It was {choice(yummy)}!")
                    for member in group:
                        member.strength *= 1.2
                else:
                    toxicity = random()
                    print(f"{repr_players(group)} ate the {' '.join(food.split(' ')[1:])}. It was uncooked!")
                    for player in group:
                        n = random()
                        if n < toxicity/3:
                            print(f"{player.name} dies of food poisoning!")
                            del self.alive_players[self.alive_players.index(player)]
                            del group[group.index(player)]
                        elif n < toxicity:
                            print(f"{player.name} is weakened from food poisoning")
                            player.strength *= (1-toxicity/4-random()/15)
                    if len(group) == 0:
                        del self.groups[self.groups.index(group)]
                del self.groups[self.groups.index(other_group)]
        else:
            for member in group:
                member.strength *= 1.2
            print(f"{repr_players(group)} ate the {' '.join(food.split(' ')[1:])}. It was {choice(yummy)}!")

    @tester
    def social(self):
        group = choice(self.groups)
        shuffle(group)
        if len(group) == 1:
            print(f"{group[0].name} was lonely and sad")
            if randint(1,10) == 1 and len(self.alive_players) > 4:
                print(f"They commited {choice(['the not alive','the no no'])}")
                del self.alive_players[self.alive_players.index(group[0])]
                del self.groups[self.groups.index(group)]

        elif len(group) == 2:
            print(f"{group[0].name} and {group[1].name} cuddled for warmth")
                
        else:
            if randint(0,1) == 0:
                print(f"{group[0].name} cuddled with {group[1].name} while {repr_players(group[2:])} watched guard")
            else:
                print(f"{repr_players(group)} had a massive orgy")

    @tester
    def sneak_on_group(self):
        if len(self.groups) == 1:
            raise Loop
        group1 = choice(self.groups)
        n = randint(0,len(self.groups)-2)
        if self.groups[n] == group1:
            n+=1
        group2 = self.groups[n]

        print(f"{repr_players(group1)} snuck up on {repr_players(group2)} to steal some stuff")

        stolen = {}

        for i in range(max(2,int(gauss(3*len(group1),0.3)))):
            p1 = choice(group1)
            p2 = choice(group2)

            if randint(1,6) == 1:
                print(f"{choice(group2).name} woke up{' and alerted the others' if len(group2) > 1 else ''}")
                self.group_fight(group1,group2,1)

                if len(group1) != 0 and len(group2) != 0:
                    if randint(1,2) == 2:
                        print(f"{repr_players(group1)} ran away!")
                    else:
                        print(f"{repr_players(group2)} ran away!")

                        if len(group1) == 0:
                            del self.groups[self.groups.index(group1)]

                        if len(group2) == 0:
                            del self.groups[self.groups.index(group2)]

                        for person in group2:
                            if not (person in stolen):
                                continue
                            for item in stolen[person]:
                                if not (item[1] in group1):
                                    if isinstance(item[0], Trap):
                                        person.add_trap(Trap)
                                    else:
                                        person.add_weapon(Weapon)
                        break
            elif randint(1,3) == 1 and len(p2.traps) != 0:
                trap = choice(p2.traps)
                if p2 in stolen:
                    stolen[p2].append((trap,p1))
                else:
                    stolen[p2] = [(trap,p1)]
                del p2.traps[p2.traps.index(trap)]
                p1.add_trap(trap)
                print(f"{p1.name} stole {p2.name}'s {trap.name}")

            elif len(p2.weapons) > 1 and len(p1.weapons) < 5:
                n = randint(0,len(p2.weapons)-2)
                if p2.weapons[n].name == 'hands':
                    n += 1
                weapon = p2.weapons[n]
                if p2 in stolen:
                    stolen[p2].append((weapon,p1))
                else:
                    stolen[p2] = [(weapon,p1)]                        
                del p2.weapons[p2.weapons.index(weapon)]
                p1.add_weapon(weapon)
                print(f"{p1.name} stole {p2.name}'s {weapon.name}")

    @tester
    def betray(self):
        l = [group for group in self.groups if len(group) > 1]
        if len(l) == 0:
            return
        group = choice(l)
        n = randint(0,len(group)-1)
        person = group[n]
        del group[n]
        self.groups.append([person])

        print(f"{person.name} betrayed {repr_players(group)} and ran away!", end = ' ')
        stolen = False
        if randint(1,5) <= 2:
            print('They took some extra food with them!')
            for p in group:
                p.strength *= 0.9
            person.strength *= 1.2
        elif randint(1,3) != 3:
            p = choice(group)
            if len(p.weapons) > 1:
                n = randint(0,len(p.weapons)-2)
                if p.weapons[n].name == 'hands':
                    n += 1
                stolen = p.weapons[n]
                del p.weapons[n]
                print(f"They took {p.name}'s {stolen.name} with them!")
                person.add_weapon(stolen)
                stolen = (stolen,p)
            else:
                return
        else:
            print()

        if randint(1,int(2+person.intelligence)) == 1:
            print(f"{choice(group).name} woke up{',' if len(group)>1 else ' and'} noticed them{' and warns the others' if len(group) > 1 else ''}!")
            self.group_fight(self.groups[-1],group,1)
            if len(group) == 0:
                del self.groups[self.groups.index(group)]
            elif len(self.groups[-1]) == 0:
                del self.groups[-1]
                if stolen:
                    if stolen[1] in self.alive_players:
                        stolen[1].add_weapon(stolen[0])
            else:
                if randint(1,2):
                    print(f'{person.name} ran away!')
                else:
                    print(f'{repr_players(group)} ran away!')

    @tester
    def insomnia(self):
        person = choice(self.alive_players)
        print(f"{person.name} is scared and has nightmares.")
        person.strength *= 0.9

    def day(self):
        print("#"*10+"Day Time"+"#"*10)

        if len(self.alive_players) == 2:
            self.groups = [[self.alive_players[0]], [self.alive_players[1]]]

        amount = max(2, int(gauss(len(self.alive_players)*0.5,0.5)))

        execute(amount,
                [self.setup_trap,100,int(len(self.alive_players)/4)+1],
                [self.animal_attack,100,int(len(self.alive_players)/6)+1],
                [self.invite,100,int(len(self.alive_players)/6)+1],
                [self.combat,100,int(len(self.alive_players)/6)+1],
                [self.random_death,0 if len(self.alive_players) <= 4 else 20,int(len(self.alive_players)/8)+1],
                [self.religion_argument,50,int(len(self.alive_players)/18)+1],
                [self.activate_trap,100,int(len(self.alive_players)/6)+1],
                [self.cornucopia,15,1],
                [self.daytime_activity,5,len(self.alive_players)],
                before = self.purge_wacky_groups,
                names = [
                    "Setup Trap",
                    "Animal Attack",
                    "Invite",
                    "Combat",
                    "Random Death",
                    "Religious Argument",
                    "Trap Activation",
                    "Cornucopia",
                    "Daytime Activity"
                ])

        try:
            self.purge_wacky_groups()
        except:
            pass

    def night(self):
        print("#"*10+"Night Time"+"#"*10)

        count = len(self.alive_players)

        ##Groups for the night are formed
        if len(self.alive_players) == 2:
            self.groups = [[self.alive_players[0]], [self.alive_players[1]]]
        
        amount = max(2,int(gauss(len(self.alive_players)*0.5,0.5)))

        execute(amount,
                [self.cook_food,100,int(count/4)],
                [self.social,50,int(count/6)],
                [self.sneak_on_group,40,int(count/7)],
                [self.betray,30,int(count/10)],
                [self.insomnia,15,int(count/5)],
                [self.activate_trap,100,int(count/12)],
                before = self.purge_wacky_groups)
        try:
            self.purge_wacky_groups()
        except:
            pass
        

    def group_fight(self,group1,group2,advantage = 0, other_lists = []):
        for i in range(max(0,int(gauss((len(group1)+len(group2)),0.5)))):
            if len(group1)==0 or len(group2)==0:
                break
            p1 = choice(group1)
            p2 = choice(group2)
            strength1 = p1.attack()+advantage
            strength2 = p2.attack()
            if random()*(strength1+strength2) <= strength1:
                if len(p1.weapons) == 1:
                    weapon = choice(p1.weapons)
                else:
                    n = randint(0,len(p1.weapons)-2)
                    if p1.weapons[n].name == "hands":
                        n += 1
                        weapon = p1.weapons[n]
                    else:
                        weapon = p1.weapons[n]
                attacker = p1.name
                victim = p2.name
                name = weapon.name
                possesive = 'their'
                pronoun = 'them'
                if random()*(strength1+1.5) <= strength1:
                    print(eval('f"'+choice(weapon.hit)+'"'))
                    del self.alive_players[self.alive_players.index(p2)]
                    for L in other_lists:
                        del L[L.index(p2)]
                    del group2[group2.index(p2)]
                else:
                    print(eval('f"'+choice(weapon.miss)+'"'))
            else:
                if len(p2.weapons) == 1:
                    weapon = choice(p2.weapons)
                else:
                    n = randint(0,len(p2.weapons)-2)
                    if p2.weapons[n].name == "hands":
                        n += 1
                        weapon = p2.weapons[n]
                    else:
                        weapon = p2.weapons[n]
                attacker = p2.name
                victim = p1.name
                name = weapon.name
                possesive = 'their'
                pronoun = 'them'
                if random()*(strength2+1.5) <= strength2:
                    print(eval('f"'+choice(weapon.hit)+'"'))
                    del self.alive_players[self.alive_players.index(p1)]
                    for L in other_lists:
                        del L[L.index(p1)]
                    del group1[group1.index(p1)]
                else:
                    print(eval('f"'+choice(weapon.miss)+'"'))


    def lake(self):
        if randint(1,4) == 1:
            m = sum([(1/p.intelligence)**2 for p in self.alive_players])
            n = random()*m
            index = -1
            while n > 0:
                index += 1
                n -= (1/self.alive_players[index].intelligence)**2
            p = self.alive_players[index]
            del self.alive_players[index]
            print(f"{p.name} drowned. What a loser")
        elif randint(1,3) == 1:
            m = sum([(30 + p.intelligence if "fishing rod" in p.inventory else 5*p.melee) for p in self.alive_players])
            n = random()*m
            index = -1
            while n > 0:
                index += 1
                n -= (30 + p.intelligence if "fishing rod" in p.inventory else 5*p.melee)
            p = self.alive_players[index]
            p.strength *= (random()/5)+1
            print(f"{p.name} caught a fish and ate it")
        elif randint(1,2) == 1:
            p = choice(self.alive_players)
            print(f"{p.name} had a swim in the lake")
        else:
            p = choice(self.alive_players)
            print(f"{p.name} had a drink of water from the lake")
            p.strength *= 1.07

    def desert(self):
        if randint(1,4) == 1:
            p = choice(self.alive_players)
            p.strength *= random()/5 + 0.8
            print(f"{p.name} is dehydrated")
        elif randint(1,3) == 1:
            p = choice(self.alive_players)
            #p.add_weapon(Weapon("Cactus Piece", 0.5, 0.3, 0.3, ))
        
    def add_player(self,player):
        self.players.append(player)
        self.kills[player] = []
        self.alive_players.append(player)

    def list_alive(self):
        newl = '\n'
        print(f'The remaining players are: {newl}{repr_players(self.alive_players)}')

    def add_weapon(self,silent=False):
        recipient = choice(self.alive_players)
        #print(self.alive_players)
        total = 0
        for weapon in weapons:
            total += weapon['weight']

        val = random()*total

        for weapon in weapons:
            val -= weapon['weight']
            if val <= 0:
                break

        name = choice(weapon['names'])
        recipient.add_weapon(Weapon(name,weapon['melee'],weapon['ranged'],weapon['intelligence'],weapon['misses'],weapon['kills']))
        if not silent:
            print("{:} found a {:}".format(recipient.name,name))
        return recipient.name, name

    def start_game(self):
        print("##########The Game Starts##########")
        n = min(len(self.players)*2,max(len(self.players),round(gauss(len(self.players)*1.5,0.2))))
        names = [p.name for p in self.players]
        d = {name:[] for name in names}
        for i in range(n):
            if randint(1,5) < 4:
                r,w = self.add_weapon(True)
            else:
                r,w = self.add_trap(True)
            d[r].append(w)
        for i in d.items():
            print("{:} found {:}".format(i[0],represent(i[1])))
        print("\n")

        self.groups = []
        for player in self.players:
            shuffle(self.groups)
            try:
                for group in self.groups:
                    if randint(1,int(len(self.players)*0.15+len(group)*2)) == 1:
                        print(f"{player.name} teams up with {repr_players(group)}")
                        group.append(player)
                        raise Loop
                self.groups.append([player])
            except:
                pass
        print('The final groups are:')
        for group in self.groups:
            print('\t'+repr_players(group))

    def add_trap(self,silent=False):
        recipient = choice(self.alive_players)
        t = choice(traps)
        name = choice(t[0])
        recipient.add_trap(Trap(name,recipient.name,t[1][0]*recipient.intelligence,t[1][1],t[1][2],t[2],t[3],t[4]))
        if not silent:
            print(f"{recipient.name} found a {name}")
        return recipient.name, name
    @tester
    def setup_trap(self):
        shuffle(self.alive_players)
        for i in self.alive_players:
            if len(i.traps) > 0:
                break
        if len(i.traps) == 0:
            raise Loop
        shuffle(i.traps)
        t = i.traps[0]
        del i.traps[0]
        name = t.name
        owner = t.owner
        possesive = 'their'
        pronoun = 'them'
        print(eval("f'"+choice(t.setup)+"'"))
        self.active_traps.append(t)
    @tester
    def activate_trap(self):
        if len(self.active_traps) == 0:
            raise Loop
        shuffle(self.active_traps)
        shuffle(self.alive_players)
        trap = self.active_traps[0]
        if trap.owner == self.alive_players[0].name:
            shuffle(self.alive_players)
        del self.active_traps[0]
        victim = self.alive_players[0].name
        owner = trap.owner
        pronoun = 'them'
        possesive = 'their'
        name = trap.name
        if random()*(self.alive_players[0].intelligence**2) <= trap.prob:
            print(eval('f"' + choice(trap.kill)+'"'))
            group = [group for group in self.groups if self.alive_players[0] in group][0]
            del group[group.index(self.alive_players[0])]
            if len(group) == 0:
                del self.groups[self.groups.index(group)]
            del self.alive_players[0]
        else:
            print(eval('f"' + choice(trap.fail)+'"'))
            self.alive_players[0].strength *= trap.strength_decrease
        try:
            del self.groups[self.groups.index([])]
        except:
            pass
        
        
g = Game()

f = open('Player-names.txt','r')
players = f.read().split('\n')
for player in load_people(hands = Weapon(*attr)):
    g.add_player(player)

print(g.players)
g.start_game()

day = 1

while len(g.alive_players) > 1:
    #print('\n##########Day ' + str(day) + '#'*10)
    print()
    g.day()
    g.night()
    g.list_alive()
    day += 1
        
output.close()