# python imports
import sys
import random
from termcolor import colored
import colorama
# file imports
from inits import Unit, Weapon, Armour, Chest

# Cards using ? attributes
# fragile, based on Arcomage card reader system
# Can read any classes, just need to know the class name, module etc 

# opens and reads file into list, used in normal object builder, DO NOT USE ALONE
def file_reader(file_name):
    file = open(file_name, "r")
    raw_data = file.readlines()
    file.close()
    return raw_data

# for converting name of class in str to actual class, used in normal object builder. DO NOT USE ALONE
def get_class(kls):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)            
    return m

# Combines above 2 funcs run this one in all cases
def object_builder(file_name, j, class_type):
    data = file_reader(file_name)
    D = get_class(class_type)
    i = 1
    big = []
    obj_at_time = []
    for item in data:
        obj_at_time.append(item.strip())
        if i % j == 0:
            adder = D(obj_at_time)
            big.append(adder)
            obj_at_time = []
        i += 1
    return big


# for initially creating items in inventory
def initial_inv_builder(holder):
    tot_weights = []
    for items in holder:
        tot_weights.append(items.weight)
    final_inv = random.choices(holder, weights=tot_weights, k=3)
    return final_inv