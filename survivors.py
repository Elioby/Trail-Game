#!/usr/bin/python3

# This file contains data about the survivors in the game

# You start with 100 HP (hit points / health points)
default_health = 100.0

# You start with $200.0
group_money = 200.0

# The MPH (miles per tick in this case) the car is curently moving at
car_speed = 40.0

group_inventory = [

	{
		"item": items["Medkit"],

		"amount": 1
	},

	{
		"item": items["Food"],

		"amount": 100
	},

]

# A list of "survivors", where the first element is the player, and the following 3 are the players friends.
# 	The names of the survivors will be added in code after the user has entered this information.
#	Realistically, this information should be initialized in code, but since there are only
#	4 survivors, and for simplicity, they are entered as data below.
#
# TODO: Should this be a dictionary itself, or just a list?
survivors = [
	{
		"name": "Survivor 1",

		"health": default_health,

		"max_health": default_health,

		"bitten": False,

		"zombified": False,

		"alive": True
	},

	{
		"name": "Survivor 2",

		"health": default_health,

		"max_health": default_health,

		"bitten": False,

		"zombified": False,

		"alive": True
	},
	
	{
		"name": "Survivor 3",

		"health": default_health,

		"max_health": default_health,

		"bitten": False,

		"zombified": False,

		"alive": True
	},
	
	{
		"name": "Survivor 4",

		"health": default_health,

		"max_health": default_health,

		"bitten": False,

		"zombified": False,

		"alive": True
	},
]