# Imports
from os import system, name
import random, sys, time
from termcolor import colored
import colorama
# File imports
from unit_builder import *
from inits import *
# Small funcs
colorama.init(autoreset=True)
# Func, clearing screen
def clear():
    if name == 'nt':
        _ = system('cls')

# Func, printing lines between text, replaces print
def line_breaker(choice=2, taken=""):
    # print empty line if given nothing
    if taken == "":
        print("")
    else:
        # 0 on top, 1 on bottom
        fill_line = colored("_" * 50, 'red')
        if choice == 0:
            print(fill_line + "\n" + taken)
        elif choice == 1:
            print(taken + "\n" + fill_line)
        elif choice == 3:
            print(fill_line + "\n" + taken + "\n" + fill_line)
        else:
            print(taken)

# Func for generating list of unique units in room, used with heat_updater
def unique_builder(room_units):
    unique_holder = []
    for item in room_units:
        if item.name not in unique_holder:
            unique_holder.append(item.name)
    return unique_holder

# NEED A LIST OF EACH UNIQUE NAME IN ROOM
# Func for changing heat, ran when you generate a room
# checks weights to simulate a bounty system, higher weights means less change to heat level
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

# enables skipping setup
power_user = True
# Welcome
def welcome_wagon():
    line_breaker()
    line_breaker(1, "Welcome to exp!")
    usr_name = input("Enter your name here: ")
    line_breaker(1, "Welcome, " + usr_name)
    return usr_name

# Running funcs to intro
if power_user is False:
    usr_name = welcome_wagon()
    junk = input("Press any key to continue: ")
else:
    usr_name = "Shane"

# Running funcs to build lists of objects
units = object_builder("units.txt", 5, "__main__.Unit") # Order doesn't matter here, add in any order you want
weapons = object_builder("weapons.txt", 4, "__main__.Weapon") # Last weapon chosen, so default for character is last in .txt
armour = object_builder("armour.txt", 4, "__main__.Armour") # Last five armour pieces in list are defaults for starting character
food = object_builder("food.txt", 3, "__main__.Food")
armour.reverse() # Reverse armour list so now first five choice in list are defaults 

# Player inits (ran once)
initial_inv = initial_inv_builder(food)
main_play = Player([usr_name, "100000000", "1000000", "100000000", [initial_inv], weapons[-1],armour[0:5]])
room_number = 0
heat = 100

# Where the fun begins
clear()
while True:
    line_breaker(1,"Room: " + str(room_number))
    # creating room
    first_room = enemy_roster(3, units, heat)
    unique_units = unique_builder(first_room)
    old_heat = heat
    heat = heat_updater(old_heat, unique_units, units)
    turn = 0
    while True:
        # Repeating each turn
        line_breaker(1, "Turn: " + str(turn))
        enemy_shower(first_room)
        # Attacking phase
        if len(first_room) >= 1:
            line_breaker(0, "Attack Phase: ")
            att_choice = input("Choose who you would like to attack: ")
            # taking / checking input
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
            # stopping items with low weights from being picked at certain points
            # Finished the room, heat, loot
            line_breaker(0, "You heat has decreased by: " + str(round(old_heat - heat, 2)))
            line_breaker(0, "You heat is now: " + str(round(heat, 2)))
            line_breaker(0, "Here is your loot:")
            a = chest_builder("training room", False, weapons, armour, food)
            for count, item in enumerate(a.contents):
                print("{}   {}".format(colored(str(count) + ".", 'yellow'), item))
            line_breaker(3, "Please choose an item or skip.")
            chosen_correct = False
            while chosen_correct is False:
                try:
                    chosen_one = int(input("Please choose an item. "))
                    main_play.inv.append(a.contents[chosen_one])
                    chosen_correct = True
                except ValueError:
                    line_breaker(1, colored("Please enter a valid id", 'red'))
            # Chaining rooms goes here
            # tmp
            line_breaker(0, "You have beaten this room, well done!\nThis should skip to next room now")
            time.sleep(2)
            clear()
            break
        turn += 1
    room_number += 1