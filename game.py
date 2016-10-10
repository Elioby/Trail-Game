#!/usr/bin/python3

import time
import screen

from debug import *
from misc_utils import *

from items import items
from cities import cities
from datetime import datetime, timedelta

# This is the main file for the trail game.

start_datetime = datetime.strptime('02/07/2009 08:00:00', '%d/%m/%Y %H:%M:%S')
current_datetime = start_datetime

distance_travelled = 0

ticks_elapsed = 0

# This is called every tick of the game
def game_tick():

    dprint("Start of game tick: " + str(ticks_elapsed))
    dprint("Current date: " + format_date(current_datetime))
    dprint("Current time: " + format_time(current_datetime))

    # Pick a random event if any (it's not going to happen most ticks, it should be relatively rare)

    global ticks_elapsed
    global current_datetime

    ticks_elapsed += 1
    current_datetime += timedelta(hours=1)

# This is the program entry point
def main():
    screen.init()
    screen.clear()

    print("Welcome to the Trail Game!")

    # TODO: Run the function that displays the "Starting Screen"

    # The main game loop
    while True:
        # Simulate one game tick
        game_tick()

        # Sleep for 1 second until we're ready to run the next tick
        time.sleep(1)


# Are we being run as a script? If so, run main().
# '__main__' is the name of the scope in which top-level code executes.
# See https://docs.python.org/3.4/library/__main__.html for explanation
if __name__ == "__main__":
    main()