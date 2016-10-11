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

ticks_elapsed = 0

# TODO: These display functions might work better in their own file
def display_starting_screen():
    # TODO: Code for the starting screen goes here
    # TODO: This function should not return until they have picked all 4 characters' names
    # TODO: These names should be updated in the survivors list in survivors.py, where survivors[0] is the main player

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

    # TODO: For each player: if player is not dead and if player is zombified: 
    # TODO:         50% chance to be shot by another survivor, 40% chance to damage another player, 10% chance to bite another survivor 

    # TODO: For each player: if player is not dead and if player is bitten and ticks_since_bitten is bigger than 4 (it's been more than 4 hours):
    # TODO:         if ticks_since_bitten is smaller than 24: (5% chance to change to zombie) else: (100% chance to change to zombie)

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

        # Sleep for 2 seconds until we're ready to run the next tick
        time.sleep(2)


# Are we being run as a script? If so, run main().
# '__main__' is the name of the scope in which top-level code executes.
# See https://docs.python.org/3.4/library/__main__.html for explanation
if __name__ == "__main__":
    main()