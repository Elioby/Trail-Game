#!/usr/bin/python3
# coding=utf-8

import items

from datetime import datetime

# This file contains data about the survivors in the game


# The date and time when the trail started
start_datetime = datetime.strptime('02/07/2009 08:00:00', '%d/%m/%Y %H:%M:%S')

# The current date and time (in game), use pass_time(hours) to change, never change directly
current_datetime = start_datetime

# Total distance travelled so far, in miles
distance_travelled = 0

# The amount of ticks gone by since the start of the game (1 tick = 1 hour)
ticks_elapsed = 0

# You start with 100 HP (hit points / health points)
default_health = 100

# You start with $40.0
group_money = 40

# The MPH (miles per tick in this case) the car is currently moving at
car_speed = 20


# TODO: write docs
def inventory_add_item(item, amount):
    item_name = item["name"]
    if item_name in group_inventory:
        group_inventory[item_name]["amount"] += amount
    else:
        group_inventory[item_name] = {"item": item, "amount": amount}


# TODO: write docs
# Returns true if it worked, false if failed
def inventory_remove_item(item, amount):
    item_name = item["name"]
    if item_name in group_inventory:
        group_item = group_inventory[item_name]
        group_item_amount = group_item["amount"]

        if group_item_amount >= amount:
            if group_item_amount == amount:
                del group_inventory[item_name]
            else:
                group_inventory[item_name]["amount"] -= amount

            return True

    return False


group_inventory = {

    "Medkit": {
        "item": items.item_list["Medkit"],

        "amount": 1
    },

    "Food": {
        "item": items.item_list["Food"],

        "amount": 100
    },

}

# A list of "survivors", where the first element is the player, and the following 3 are the players friends.
# 	The names of the survivors will be added in code after the user has entered this information.
#	Realistically, this information should be initialized in code, but since there are only
#	4 survivors, and for simplicity, they are entered as data below.
survivor_list = [
    {
        "name": "Survivor 1",

        "health": default_health,

        "max_health": default_health,

        "bitten": False,

        "ticks_since_bitten": 0,

        "zombified": False,

        "alive": True
    },

    {
        "name": "Survivor 2",

        "health": default_health,

        "max_health": default_health,

        "bitten": False,

        "ticks_since_bitten": 0,

        "zombified": False,

        "alive": True
    },

    {
        "name": "Survivor 3",

        "health": default_health,

        "max_health": default_health,

        "bitten": False,

        "ticks_since_bitten": 0,

        "zombified": False,

        "alive": True
    },

    {
        "name": "Survivor 4",

        "health": default_health,

        "max_health": default_health,

        "bitten": False,

        "ticks_since_bitten": 0,

        "zombified": False,

        "alive": True
    },
]
