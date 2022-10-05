# Imports of py modules
import random

# Class of enemies
class Unit(object):
    def __init__(self, name, atk, defen, hp):
        self.name = name
        self.atk = int(atk)
        self.defen = int(defen)
        self.hp = int(hp)
    
    def __str__(self):
        return ("{} {} {} {}".format(self.name, self.atk, self.defen, self.hp))
    
    # FATAL ERROR, THE KAMINO EFFECT
    # WHEN CREATING ROOMS, DAMAGE AGAINST ONE MEANS DAMAGE AGAINST ALL
    # ENEMIES NEED TO BE INDIVIDUALS, NOT CLONES 
    # (SOLUTION) MAYBE CREATE NEW OBJS WHEN RUNNING THE ROOM-BUILDER, THIS VERY BAD THOUGH
    def damage_take(self, other):
        if self.defen >= other.atk:
            print("They took no damage!")
            return
        else:
            self.hp = self.hp - (other.atk - self.defen)
            print("They took: {} damage and have {} health left".format(other.atk - self.defen, self.hp))

# Class for weapons
class Weapon(object):
    def __init__(self, name, type, damage):
        self.name = name
        self.type = type
        self.damage = int(damage)
    
    def __str__(self):
        return ("{} {} {}".format(self.name, self.type, self.damage))

# Class for armour
class Armour(object):
    def __init__(self, name, type, protection):
        self.name = name
        self.type = type
        self.protection = int(protection)

    def __str__(self):
        return ("{} {} {}".format(self.name, self.type, self.protection))


# Class for player stats
class Player(object):
    def __init__(self, name, atk, defen, hp, inv, weapon, armour):
        self.name = name
        self.atk = int(atk)
        self.defen = int(defen)
        self.hp = int(hp)
        self.inv = inv
        self.weapon = weapon
        self.armour = armour
    
    def __str__(self):
        return ("{} {} {} {} {}\n{}\n{}".format(self.name, self.atk, self.defen, self.hp, self.inv, self.weapon, self.armour))

# Function for generating the enemy roster for a room
# General case, Boss Rooms need separate function
# No inclusion of weight, see issue with reading in unit_builder
# Room size <-> amount of enemies, units <-> list of unit objects to pick from
def enemy_roster(room_size, units):
    roster = []
    while len(roster) < room_size:
        choice = random.randint(1, len(units))
        choice = choice - 1
        roster.append(units[choice])
    return roster

# Function for showing current enemies
# Player showing kept seperate
def enemy_shower(enemy_list):
    print("You are fighting these enemies:")
    for count, item in enumerate(enemy_list):
        print("{}.  {:<15}  |  Health: {}".format(count, item.name, item.hp))