# Module Imports
import copy
import random
from termcolor import colored
import colorama
from os import system

# Misc Imports
# Colorama
# This needed here?
colorama.init(autoreset=True)

# Class Definitions
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
    # basic calulation, need more work with defence values (maybe copy fnv's dt system?)
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


# Heat related functions
# Functions for generating list of unique units in room, used with heat_updater
def unique_builder(room_units):
    unique_holder = []
    for item in room_units:
        if item.name not in unique_holder:
            unique_holder.append(item.name)
    return unique_holder

# Function for changing heat, ran when you generate a room
# Checks weights to simulate a bounty system, higher weights means less change to heat level
def heat_updater(heat, uniques, units):
    orig = heat
    current_heat = heat
    for each in uniques:
        for i in units:
            if i.name == each:
                calc = round((orig / i.weight) * 0.1, 2) # for changing heat meter
                weight_calc = calc / 10 # for changing the weights of units, higher weight means unit loses some chance of being picked
                heat -= calc
                if heat > 10:
                    if i.weight > weight_calc and i.weight > 1:
                            # can be adjusted
                            i.weight -= weight_calc
                            i.weight = round(i.weight, 2)
                    else:
                        # has reached min weight, keep at 1
                        i.weight = 1
                else:
                    print("Heat has reached its minimum, correcting to 10")
                    return 10
    return heat


# Function for generating the enemy roster for a room
# General case, Boss Rooms need separate function
def enemy_roster(room_size, units, heat):
    unit_weights = []
    for item in units:
        unit_weights.append(item.weight)
    
    roster = []
    while len(roster) < room_size:
        got_good = False
        while got_good is False:
            # Probably dont need this while got_good anymore,
            # Was only needed for the weight limit system, which is now gone
            choice = random.choices(units, weights=unit_weights, k=1)
            print(choice[0].name)
            got_good = True
        # Anti Kamino System
        roster.append(copy.deepcopy(choice[0]))
    return roster

# Function for showing current enemies
# Player showing kept separate
def enemy_shower(enemy_list):
    if len(enemy_list) <= 0:
        print("This room is empty.....") # prints when room is empty
    else:
        print("    You are fighting these enemies:\n")
        for count, item in enumerate(enemy_list):
            if count < 10 and len(enemy_list) > 9:
                count = "0" + str(count)
            # dont make names of enemies really long (like 100 chars) as breaks this format
            # Hate this solution, too fragile
            print("{:<5}  {:<15}  |  Health: {:<5} {}".format(colored(str(count) + ".",'yellow'), item.name, item.hp, item.weight))

# Function for building chest with loot,
# is_boss not implemented
# Always 3 items for now, takes from weapon, armour, food
# Customise this later
def chest_builder(room, is_boss, weapons, armour, food):
    total_items = weapons + armour + food
    loot_weights = []
    for item in total_items:
        loot_weights.append(int(item.weight))
    final_loot = random.choices(total_items, weights=loot_weights, k=3)
    return Chest(room, final_loot, is_boss)