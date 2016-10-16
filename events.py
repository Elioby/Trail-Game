#!/usr/bin/python3
# coding=utf-8

import screen
import survivors

from misc_utils import *


# This file contains data and functions about the random events defined in the game

# This is an example event function, it runs screen.print_notification to notify the player of a short message, return false if cancelled
def event_bitten_by_zombie():
    random_survivor = get_random_survivor(False, False, False, False)

    if random_survivor is not None:
        random_survivor["bitten"] = True

        screen.print_notification(random_survivor["name"] + " was bitten by a zombie.")

        return True

    return False


def event_whiplash():
    survivor_count = count_survivors(True, True, False, False)

    for survivor in survivors.survivor_list:
        if survivor["alive"] and not survivor["zombified"]:
            survivor["health"] -= 10

    if survivor_count > 1:
        party_identifier = "everyone gets"
    else:
        party_identifier = "you get"

    screen.print_notification("You swerve quickly to avoid hitting a zombie and " + party_identifier + " whiplash.")

    return True


# TODO: Should this be a dictionary itself, or just a list?
# TODO: Events should start off simple: "<random survivor> got bitten by a zombie"
events = [

    {
        # The percentage chance for this event to happen
        "occurrence_chance": 0.5,

        # A function to run when the event occurs
        "notification_handler_function": event_bitten_by_zombie
    },

    {
        # The percentage chance for this event to happen
        "occurrence_chance": 1.0,

        # A function to run when the event occurs
        "notification_handler_function": event_whiplash
    },

]
