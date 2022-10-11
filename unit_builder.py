from inits import Unit, Weapon, Armour, Chest
# Cards using ? attributes
# fragile, based on Arcomage card reader system

# using attrib name, atk, def, hp, specs(later)?
#opens and reads file into list, used in other builders, DO NOT USE ALONE
def file_reader(file_name):
    file = open(file_name, "r")
    raw_data = file.readlines()
    file.close()
    return raw_data

# THIS DOES NOT WORK
# THINK OF WAYS TO DYNAMICALLY GENERATE DATA ITEMS TO SPLIT IN object_builder func (pointer)
# Takes data and amount of items per obj, creates obj and return as list of obj, DO NOT USE ALONE, THE 
def object_builder(data, j):
    i = 0
    big = []
    for item in data:
        if i % j == 0:
            adder = Unit(data[i - 4].strip(), data[i - 3].strip(), data[i - 2].strip(), data[i - 1].strip()) # maybe want to rewrite this as a loop, going backward?
            big.append(adder)
        i += 1
    return big
    
    #a = object_builder(raw_data, 4)
    #return a

# Order does matter here, cant remember exact details figure it out later
# For reading in units
def u_builder(file_name):
    data = file_reader(file_name)
    # generic quick fix
    i = 0
    big = []
    for item in data:
        if i % 5 == 0:
            adder = Unit(data[i - 5].strip(), data[i - 4].strip(), data[i - 3].strip(), data[i - 2].strip(), data[i - 1].strip())
            big.append(adder)
        i += 1
    return big
    #a = object_builder(raw_data, 4)
    #return a


#For reading in player weapons
def weapon_builder(file_name):
    data = file_reader(file_name)
    #generic quick fix
    i = 0
    big = []
    for item in data:
        if i % 4 == 0:
            adder = Weapon(data[i - 4].strip(), data[i - 3].strip(), data[i - 2].strip(), data[i - 1].strip())
            big.append(adder)
        i += 1
    return big
    #a = object_builder(raw_data, 3)
    #return a

#For reading in armour pieces
def armour_builder(file_name):
    data = file_reader(file_name)
    #generic quick fix
    i = 0
    big = []
    for item in data:
        if i % 4 == 0:
            adder = Armour(data[i - 4].strip(), data[i - 3].strip(), data[i - 2].strip(), data[i - 1].strip())
            big.append(adder)
        i += 1
    return big
    #a = object_builder(raw_data, 3)
    #return a