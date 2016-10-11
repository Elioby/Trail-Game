#!/usr/bin/python3

import time
import screen
import random

from debug import *
from misc_utils import *

from items import items
from events import events
from cities import cities
from survivors import survivors, car_speed
from datetime import datetime, timedelta

# This is the main file for the trail game.

# The date and time when the trail started 
start_datetime = datetime.strptime('02/07/2009 08:00:00', '%d/%m/%Y %H:%M:%S')

# The current date and time (in game)
current_datetime = start_datetime

# Total distance travelled so far, in miles 
distance_travelled = 0

# The amount of ticks gone by since the start of the game (1 tick = 1 hour)
ticks_elapsed = 0

# TODO: These display functions might work better in their own file
def display_starting_screen():
    # TODO: Code for the starting screen goes here
    # TODO: This function should not return until they have picked all 4 characters' names
    # TODO: These names should be updated in the survivors list in survivors.py, where survivors[0] is the main player

    # TODO: use the input function to ask for the players name, and for three other friends they can count on eg: input("What is your name? ")

    # TODO: update the names in survivors.py by using the survivors list eg: survivors[0] = player_name

    pass

def display_dead_screen():
    # TODO: Code for the dead screen goes here
    # TODO: This function should never return (use quit() ? unless that's a bad idea for some reason)

    pass

def display_city_screen():
    # TODO: Code for the city screen goes here
    # TODO: This function should not return until they leave the city

    pass

# This is called every tick of the game
def game_tick():
    global ticks_elapsed
    global current_datetime
    global distance_travelled

    # TODO: Check if the player is dead, if so, show the dead screen
    # TODO: display_dead_screen()

    dprint("Start of game tick: " + str(ticks_elapsed))
    dprint("Current date: " + format_date(current_datetime))
    dprint("Current time: " + format_time(current_datetime))

    # TODO: Pick a random event if any (it's not going to happen most ticks, it should be relatively rare)
    event_random = random.uniform(0.0, 100.0)

    for event in events:
        if event["occurrence_chance"] > event_random:
            event_function = None

            if event["notification_handler_function"] is not None:
                event_function = event["notification_handler_function"]

            # TODO: Add support for other handler functions that are more complex than a notification

            if event_function is not None:
                notification = event_function()

                if notification != None:
                    dprint(notification)


    # TODO: If the current time is 8pm, do food consumption
    if current_datetime.hour == 20:
        dprint("Do food consumption")

    for survivor in survivors:
        if survivor["alive"] and survivor["zombified"]:
            random_number = random.randrange(1, 100)
            random_survivor = get_random_survivor()

            if random_number <= 50:
                survivor["alive"] = False

                # TODO: show as notification
                # TODO: subtract a bullet from ammo?
                dprint(random_survivor["name"] + " managed to shoot a zombified " + survivor["name"] + " dead.")
            elif random_number <= 90:
                random_damage = random.randrange(1, 20)

                random_survivor["health"] -= random_damage 

                # TODO: show as notification
                dprint("A zombified " + survivor["name"] + " damaged " + random_survivor["name"] + " for " + str(random_damage) + " damage.")
            else:
                # TODO: bite another survivor

                # TODO: show as notification
                dprint()



    for survivor in survivors:
        if survivor["alive"] and survivor["bitten"] and not survivor["zombified"]:
            ticks_since_bitten = survivor["ticks_since_bitten"]

            if ticks_since_bitten > 4:
                should_turn = False

                if ticks_since_bitten < 24:
                    random_number = random.randrange(1, 100)

                    should_turn = random_number <= ticks_since_bitten * 2
                else:
                    should_turn = True

                if should_turn:
                    # TODO: show as notification
                    survivor["zombified"] = True

                    dprint(survivor["name"] + " turned into a zombie.")

            survivor["ticks_since_bitten"] = ticks_since_bitten + 1

    # TODO: If distance to next city is smaller than car_speed, show city screen
    # TODO: display_city_screen()

    ticks_elapsed += 1
    current_datetime += timedelta(hours=1)
    distance_travelled += car_speed

# This is the program entry point
def main():
    screen.init()
    screen.clear()

    print("Welcome to the Trail Game!")

    display_starting_screen()

    # The main game loop
    while True:
        # Simulate one game tick
        game_tick()

        # Sleep for 1 second until we're ready to run the next tick
        time.sleep(2)
        screen.set_cursor(10, 10)


# Are we being run as a script? If so, run main().
# '__main__' is the name of the scope in which top-level code executes.
# See https://docs.python.org/3.4/library/__main__.html for explanation
if __name__ == "__main__":
    main()