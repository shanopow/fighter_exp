# Imports
from os import system, name
import random, sys, time

# File imports
from unit_builder import *
from inits import *

# Small funcs
# Func, clearing screen
def clear():
    if name == 'nt':
        _ = system('cls')

# Func, printing lines between text, replaces print
def line_breaker(choice=2, taken=""):
    #empty
    if taken == "":
        print("")
    else:
        # 0 on top, 1 on bottom
        if choice == 0:
            print("_" * 50 + "\n" + taken)
        elif choice == 1:
            print(taken + "\n" + "_" * 50)
        elif choice == 3:
            print("_" * 50 + "\n" + taken + "\n" + "_" * 50)
        else:
            print(taken)


# enable to skip
power_user = False
# Welcome
def welcome_wagon():
    line_breaker()
    line_breaker(1, "Welcome to exp!")
    usr_name = input("Enter your name here: ")
    line_breaker(1, "Welcome, " + usr_name)
    return usr_name

# Running funcs to intro
if power_user is True:
    usr_name = welcome_wagon()
    junk = input("Press any key to continue: ")
else:
    usr_name = "Shane"

# Running funcs to build lists of objects
units = object_builder("units.txt", 5, "__main__.Unit") # Order doesn't matter here, add in any order you want
weapons = object_builder("weapons.txt", 4, "__main__.Weapon") # Last weapon chosen, so default for character is last in .txt
armour = object_builder("armour.txt", 4, "__main__.Armour") # Last five armour pieces in list are defaults for starting character
armour.reverse() # Reverse armour list so now first five choice in list are defaults 

# Player init
main_play = Player([usr_name, "100", "1", "10", ["Apple", "Banana", "Apple"], weapons[-1],armour[0:5]])
# Turn counter
turn = 0
clear()
heat = 0
# NOT FINAL SECTION JUST FOR ONE TRAINING ROOM, WILL MOVE TO FUNC LATER
line_breaker(1, "Welcome to the training room.")
# creating rooms
first_room = enemy_roster(5, units)
# heat counter, ran after room generation
# weight checker meant to simulate a bounty system, but 10 is arbitrary value, maybe beter griffin way?
old_heat = heat
for item in first_room:
    if item.weight < 10:
        heat += item.weight
# Where the fun begins
while True:
    # Repeating each turn
    line_breaker(1, "Turn: " + str(turn))
    enemy_shower(first_room)
    # Attacking phase
    if len(first_room) >= 1:
        line_breaker(0, "Attack Phase: ")
        att_choice = input("Choose who you would like to attack: ")
        # taking / checking input s
        if att_choice.isdecimal() is True:
            first_room[int(att_choice)].damage_take(main_play, first_room)

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
        # Finished the room, heat, loot
        line_breaker(0, "You heat has increased by: " + str(heat - old_heat))
        line_breaker(0, "You heat is now: " + str(heat))
        line_breaker(0, "Here is your loot:")
        a = chest_builder("training room", False, weapons, armour)
        for count, item in enumerate(a.contents):
            print("{}.   {}".format(count, item))
        line_breaker(3, "Please choose an item or skip.")
        chosen_correct = False
        while chosen_correct is False:
            try:
                chosen_one = int(input("Please choose an item. "))
                chosen_correct = True
            except ValueError:
                line_breaker(1, "Please enter the id of an item")
        # Chaining rooms goes here
        # tmp
        line_breaker(0, "You have beaten this room, well done!\nToo bad the line ends here for now. Goodbye!")
        quit()
    turn += 1