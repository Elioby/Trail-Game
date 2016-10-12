#!/usr/bin/python3

# This file contains data on the screens in the game

import screen

from misc_utils import *

# TODO: These are currently useless because of the front buffer, maybe they won't be in future though?
previous_screen = None
current_screen = None

def set_current_screen(screen):
	global previous_screen
	global current_screen

	previous_screen = current_screen
	current_screen = screen

# TODO: These display functions might work better in their own file
def draw_starting_screen():
    # TODO: Code for the starting screen goes here
    # TODO: This function should not return until they have picked all 4 characters' names
    # TODO: These names should be updated in the survivors list in survivors.py, where survivors[0] is the main player

    # TODO: use the input function to ask for the players name, and for three other friends they can count on eg: input("What is your name? ")

    # TODO: update the names in survivors.py by using the survivors list eg: survivors[0] = player_name

    set_current_screen(screens["starting"])
    
    screen.clear()

    print("This is the starting screen")

    wait_key()

def draw_dead_screen():
    # TODO: Code for the dead screen goes here
    # TODO: This function should never return (use quit() ? unless that's a bad idea for some reason)

    # TODO: Replace with something else
    set_current_screen(screens["dead"])

    screen.clear()

    print("You died!")

    quit()

def draw_city_screen(city):
    # TODO: Code for the city screen goes here
    # TODO: This function should not return until they leave the city

    # TODO: Replace with something else
    set_current_screen(screens["city"])

    screen.clear()

    ingored_input = input("You are in " + city["name"] + ", what would you like to do? ")



def draw_travelling_screen():
    set_current_screen(screens["travelling"])

    screen.clear()

    print("This is the travelling screen")

screens = {
	"starting": {
		"name": "starting",

		"draw_function": draw_starting_screen
	},

	"dead": {
		"name": "dead",

		"draw_function": draw_dead_screen
	},

	"city": {
		"name": "city",

		"draw_function": draw_city_screen
	},

	"travelling": {
		"name": "travelling",

		"draw_function": draw_travelling_screen
	},
}
