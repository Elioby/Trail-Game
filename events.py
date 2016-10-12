#!/usr/bin/python3

from misc_utils import *


# This file contains data and functions about the random events definined in the game

# This is an example event function, it returns the message to notify the player with, return None to cancel the event
def event_bitten_by_zombie():
    if count_survivors(False, False, False, False) == 0:
        return None

    random_survivor = get_random_survivor(False, False, False, False)

    random_survivor["bitten"] = True

    return random_survivor["name"] + " was bitten by a zombie."


# TODO: Should this be a dictionary itself, or just a list?
# TODO: Think more about the data structure of events, it could end up being fairly complex
# TODO: Events should start off simple: "<random survivor> got bitten by a zombie"
events = [

    {
        # The percentage chance for this event to happen
        # TODO: change this back to a small percentage, this is just for testing
        "occurrence_chance": 10.0,

        "notification_handler_function": event_bitten_by_zombie
    },

]
