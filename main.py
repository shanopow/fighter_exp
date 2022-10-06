# Imports
from os import system, name
import random
import time
# File imports
from unit_builder import *
from inits import *

# Small funcs
# Func, clearing screen
def clear():
    if name == 'nt':
        _ = system('cls')

# Func, printing breaks with content as first line (Needs start line as prog cant print like that)
def  line_breaker(choice=2, taken=""):
    #empty
    if taken == "":
        print("")
    else:
        # 0 on top, 1 on bottom
        if choice == 0:
            print("_" * 35 + "\n" + taken)
        elif choice == 1:
            print(taken + "\n" + "_" * 35)
        else:
            print(taken)


# Welcome, intro map
def welcome_wagon():
    line_breaker()
    line_breaker(1, "Welcome to exp!")
    usr_name = input("Enter your name here: ")
    line_breaker(1, "Welcome, " + usr_name)
    return usr_name

# Running funcs to intro
# Reading in lists 
usr_name = welcome_wagon()
units = u_builder("units.txt") # Order doesn't matter here, add in any order you want
weapons = weapon_builder("weapons.txt") # Last weapon chosen, so default for character is last in .txt
armour = armour_builder("armour.txt") # Last five armour pieces in list are defaults for starting character
armour.reverse() # reverse armour list so now first five choice in list are defaults 

# Player init
main_play = Player(usr_name, "1", "1", "10", ["Apple", "Banana", "Apple"], weapons[-1],armour[0:5])

# Turn counter
turn = 0
junk = input("Press any key to continue: ")
clear()

# NOT FINAL SECTION JUST FOR ONE TRAINING ROOM, WILL MOVE TO FUNC LATER
line_breaker(1, "Welcome to the training room.")
first_room = enemy_roster(10, units)

# Where the fun begins
while True:
    line_breaker(1, "Turn: " + str(turn))
    enemy_shower(first_room)
    line_breaker()
    #Attacking phase
    print("Attack phase:")
    att_choice = int(input("Choose who you would like to attack: "))
    first_room[att_choice].damage_take(main_play)
    # Defending Phase
    line_breaker(0, "Defending Phase:")
    # End Turn
    cont = input("_" * 50 + "\n End turn? ")
    clear()
    turn += 1