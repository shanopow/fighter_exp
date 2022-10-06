# Imports of py modules
import random
import copy

# Class of enemies
class Unit(object):
    def __init__(self, name, atk, defen, hp):
        self.name = name
        self.atk = int(atk)
        self.defen = int(defen)
        self.hp = int(hp)
    
    def __str__(self):
        return ("{} {} {} {}".format(self.name, self.atk, self.defen, self.hp))

    # damage taken calculator (basic calulation, need more work with defence values)
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
                # BAD WAY OF FINDING OBJECT TO DELETE, NEED BETTER WAY OF INDEXING TO IT
                for count, item in enumerate(holder):
                    if item is self:
                        holder.pop(count)
                        break
            # normal damage calulations
            else:
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

    def damage_taken(self, enemies):
        for item in enemies:
            # no damage
            if self.defen >= (item.atk):
                print("We took no damage from", item.name)
            else:
                self.hp = self.hp - (item.atk- self.defen)
                # took damage
                if self.hp <= 0:
                    print("You have no health left, you died!")
                    return False
                else:
                    print("We took: {} damage from {} and have {} health left".format(item.atk - self.defen, item.name, self.hp))
        return True


# Function for generating the enemy roster for a room
# General case, Boss Rooms need separate function
# No inclusion of weight, see issue with reading in unit_builder
# Room size <-> amount of enemies, units <-> list of unit objects to pick from
def enemy_roster(room_size, units):
    roster = []
    while len(roster) < room_size:
        choice = random.randint(1, len(units))
        choice = choice - 1
        roster.append(copy.deepcopy(units[choice]))
    return roster

# Function for showing current enemies
# Player showing kept seperate
def enemy_shower(enemy_list):
    print("You are fighting these enemies:")
    for count, item in enumerate(enemy_list):
        print("{}.  {:<15}  |  Health: {}".format(count, item.name, item.hp))