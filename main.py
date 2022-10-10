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

# Func, printing breaks
def  line_breaker(choice=2, taken=""):
    #empty
    if taken == "":
        print("")
    else:
        # 0 on top, 1 on bottom
        if choice == 0:
            print("_" * 50 + "\n" + taken)
        elif choice == 1:
            print(taken + "\n" + "_" * 50)
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
armour.reverse() # Reverse armour list so now first five choice in list are defaults 

# Player init
main_play = Player(usr_name, "100", "1", "10", ["Apple", "Banana", "Apple"], weapons[-1],armour[0:5])
# Turn counter
turn = 0
junk = input("Press any key to continue: ")
clear()
# NOT FINAL SECTION JUST FOR ONE TRAINING ROOM, WILL MOVE TO FUNC LATER
line_breaker(1, "Welcome to the training room.")
first_room = enemy_roster(1, units)

# Where the fun begins
while True:
    # Repeating each turn
    line_breaker(1, "Turn: " + str(turn))
    enemy_shower(first_room)
    # Attacking phase
    if len(first_room) >= 1:
        line_breaker(0, "Attack Phase: ")
        att_choice = int(input("Choose who you would like to attack: "))
        first_room[att_choice].damage_take(main_play, first_room)
    
        # Defending Phase
        line_breaker(0, "Defending Phase:")
        # Taking damage
        killed_check = main_play.damage_taken(first_room)
        if killed_check is False:
            quit()

        # End Turn
        cont = input("_" * 50 + "\n End turn? ")
        clear()
    else:
        #Finished the room, loot
        line_breaker(0, "Here is your loot:")
        a = chest_builder("training room", False, weapons, armour)
        for item in a.contents:
            print(item)
        line_breaker(0, "Please choose an item or skip")
        loot_choice = input("Would you like to choose item 1, item 2, or skip? (1/2/3) ")
        if loot_choice == "1":
            main_play.weapon = a.contents[0]
        if loot_choice == "2":
            main_play.armour = a.contents[1]
        # Chaining rooms goes here
        
        #tmp
        line_breaker(0, "You have beaten this room, well done!\nToo bad the line ends here for now. Goodbye!")
        quit()
    turn += 1