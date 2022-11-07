# Imports of py modules
import copy
import random
from termcolor import colored
import colorama
from os import system
# junk
colorama.init(autoreset=True)
# Class of loot chests
class Chest(object):
    def __init__(self, room, contents, is_boss):
        self.room = room
        self.contents = contents
        self.is_boss = is_boss
    
    def __str__(self):
        return "This chest contains {}".format(self.contents)


# Class of enemies
class Unit(object):
    def __init__(self, holder):
        self.name = holder[0]
        self.atk = int(holder[1])
        self.defen = int(holder[2])
        self.hp = int(holder[3])
        self.weight = int(holder[4])

    def __str__(self):
        return ("{} {} {} {} ({})".format(self.name, self.atk, self.defen, self.hp, self.weight))

    # damage taken calculator
    # basic calulation, need more work with defence values
    def damage_take(self, other, holder):
        # no damage
        if self.defen >= (other.atk * other.weapon.damage):
            print("They took no damage!")
            return
        else:
            self.hp = self.hp - ((other.atk * other.weapon.damage) - self.defen)
            # killed enemy
            if self.hp <= 0:
                print("You have destroyed them!")
                # BAD WAY OF FINDING OBJECT TO DELETE, NEED BETTER WAY OF INDEXING DIRECTLY TO IT
                for count, item in enumerate(holder):
                    if item is self:
                        holder.pop(count)
                        break
            # normal damage calulations
            else:
                print("They took: {} damage and have {} health left".format(other.atk - self.defen, self.hp))

# Class for weapons
class Weapon(object):
    def __init__(self, holder):
        self.name = holder[0]
        self.i_type = holder[1]
        self.damage = int(holder[2])
        self.weight = int(holder[3])
    
    def __str__(self):
        return ("{: <20} {: <10} {} ({})".format(self.name, self.i_type, self.damage, self.weight))

# Class for armour
class Armour(object):
    def __init__(self, holder):
        self.name = holder[0]
        self.i_type = holder[1]
        self.protection = int(holder[2])
        self.weight = holder[3]

    def __str__(self):
        return ("{: <20} {: <10} {} ({})".format(self.name, self.i_type, self.protection, self.weight))

# Class for food in inventory
class Food(object):
    def __init__(self, holder):
        self.name = holder[0]
        self.healing = holder[1]
        self.weight = int(holder[2])

    def __str__(self):
        return "{: <20} {: <10} ({})".format(self.name, self.healing, self.weight)

# Class for player stats
class Player(object):
    def __init__(self, holder):
        self.name = holder[0]
        self.atk = int(holder[1])
        self.defen = int(holder[2])
        self.hp = int(holder[3])
        self.inv = holder[4]
        self.weapon = holder[5]
        self.armour = holder[6]

    def __str__(self):
        return ("{} {} {} {} {}\n{}\n{}".format(self.name, self.atk, self.defen, self.hp, self.inv, self.weapon, self.armour))

    def damage_taken(self, enemies):
        for item in enemies:
            # no damage
            if self.defen >= (item.atk):
                print("We took no damage from", item.name)
            else:
                self.hp = self.hp - (item.atk- self.defen)
                # took damage
                if self.hp <= item.atk:
                    print("You have no health left, you died!")
                    return False
                else:
                    print("We took: {} damage from {} and have {} health left".format(item.atk - self.defen, item.name, self.hp))
        return True


# Function for generating the enemy roster for a room
# General case, Boss Rooms need separate function
# Room size: amount of enemies
# Units: list of unit objects to pick from

def enemy_roster(room_size, units, heat):
    # make list of weights for generating rooms
    unit_weights = []
    for item in units:
        unit_weights.append(item.weight)
    roster = []
    while len(roster) < room_size:
        got_good = False
        while got_good is False:
            # keep choosing until we find good unit to put in
            choice = random.choices(units, weights=unit_weights, k=1)
            print(choice[0].name)
            got_good = True
        roster.append(copy.deepcopy(choice[0]))
    return roster

# Function for showing current enemies
# Player showing kept seperate
def enemy_shower(enemy_list):
    if len(enemy_list) <= 0:
        print("This room is empty.....") # shower only if room now empty
    else:
        print("    You are fighting these enemies:\n")
        for count, item in enumerate(enemy_list):
            if count < 10 and len(enemy_list) > 9:
                count = "0" + str(count)
            # dont make names of enemies really long (like 100 chars) as breaks this format
            print("{:<5}  {:<15}  |  Health: {:<5} {}".format(colored(str(count) + ".",'yellow'), item.name, item.hp, item.weight))

# for building loot of chest and adding as an object
def chest_builder(room, is_boss, weapons, armour, food):
    total_items = weapons + armour + food
    loot_weights = []
    for item in total_items:
        loot_weights.append(int(item.weight))
    final_loot = random.choices(total_items, weights=loot_weights, k=3)
    return Chest(room, final_loot, is_boss)
