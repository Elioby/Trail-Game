#!/usr/bin/python3
# coding=utf-8
import game
import items
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


def event_sits_on():
    random_survivor = get_random_survivor(False, True, False, False)

    if random_survivor is not None:
        random_item = get_random_dict_value(survivors.group_inventory)

        if random_item is not None:
            random_item_amount = 1

            if random_item["item"]["min_value"] <= 10:
                random_item_amount = random.randrange(11 - random_item["item"]["min_value"], 15 - random_item["item"]["min_value"])

            if random_item["amount"] < random_item_amount:
                random_item_amount = random_item["amount"]

            survivors.inventory_remove_item(random_item["item"], random_item_amount)

            screen.print_notification(random_survivor["name"] + " sits on " + str(random_item_amount) + " " + random_item["item"]["name"] + " and ruins it.")
            return True

    return False


def event_vending_machine():
    survivors.inventory_add_item(items.item_list["Food"], random.randrange(5, 20))
    screen.print_notification("You take some food from a vending machine.")

    return True


def event_rotting_food():
    if survivors.inventory_remove_item(items.item_list["Food"], random.randrange(5, 20)):
        screen.print_notification("Some of your food gives off a bad smell. You throw it out just to be safe.")
        return True

    return False


def event_fake_fuel():
    if "Fuel" in survivors.group_inventory:
        if survivors.group_inventory["Fuel"]["amount"] >= 10:
            survivors.group_inventory["Fuel"]["amount"] -= 10
            screen.print_notification("You find one of your fuel cans is actually filled with water.")
            return True

    return False


def event_zombie_tear():
    screen.print_notification("You watch on as a zombie tears into something, or someone...")

    return True


def event_fog():
    screen.print_notification("You head into an area of heavy fog and have to drive slowly.")

    survivors.foggy = True
    survivors.car_speed = 5

    return True


def event_fog_clear():
    if survivors.foggy:
        screen.print_notification("The sky clears up and you return to normal driving speed")

        survivors.foggy = False
        survivors.car_speed = 20

        return True

    return False


def event_admire_scenery():
    random_survivor = get_random_survivor(False, True, False, False)

    if random_survivor is not None:
        screen.print_notification(random_survivor["name"] + " wants to stop for an hour to admire the scenery.")

        game.pass_time(1, False)


events_list = [

    {
        # The percentage chance for this event to happen
        "occurrence_chance": 2.0,

        # A function to run when the event occurs
        "notification_handler_function": event_bitten_by_zombie
    },

    {
        # The percentage chance for this event to happen
        "occurrence_chance": 3.0,

        # A function to run when the event occurs
        "notification_handler_function": event_whiplash
    },

    {
        # The percentage chance for this event to happen
        "occurrence_chance": 1.0,

        # A function to run when the event occurs
        "notification_handler_function": event_sits_on
    },

    {
        # The percentage chance for this event to happen
        "occurrence_chance": 3.0,

        # A function to run when the event occurs
        "notification_handler_function": event_fake_fuel

    },

    {
        # The percentage chance for this event to happen
        "occurrence_chance": 1.0,

        # A function to run when the event occurs
        "notification_handler_function": event_vending_machine

    },

    {
        # The percentage chance for this event to happen
        "occurrence_chance": 2.0,

        # A function to run when the event occurs
        "notification_handler_function": event_rotting_food

    },

    {
        # The percentage chance for this event to happen
        "occurrence_chance": 3.0,

        # A function to run when the event occurs
        "notification_handler_function": event_zombie_tear

    },

    {
        # The percentage chance for this event to happen
        "occurrence_chance": 1.0,

        # A function to run when the event occurs
        "notification_handler_function": event_fog

    },

    {
        # The percentage chance for this event to happen
        "occurrence_chance": 20.0,

        # A function to run when the event occurs
        "notification_handler_function": event_fog_clear

    },

    {
        # The percentage chance for this event to happen
        "occurrence_chance": 2.0,

        # A function to run when the event occurs
        "notification_handler_function": event_admire_scenery

    },

]
