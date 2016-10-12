#!/usr/bin/python3

import screen
import screens

from debug import *
from misc_utils import *

from events import events
import survivors
from datetime import datetime, timedelta

# This is the main file for the trail game.

# The date and time when the trail started 
start_datetime = datetime.strptime('02/07/2009 08:00:00', '%d/%m/%Y %H:%M:%S')

# The current date and time (in game), use pass_time(hours) to change, never change directly
current_datetime = start_datetime

# Total distance travelled so far, in miles 
distance_travelled = 0

# The amount of ticks gone by since the start of the game (1 tick = 1 hour)
ticks_elapsed = 0


# You must use this method when changing the time
def pass_time(hours):
    global ticks_elapsed
    global current_datetime
    global distance_travelled

    # TODO: If the current time is 8pm, do food consumption
    if current_datetime.hour == 20 or (int(current_datetime.hour) < 20 < int(current_datetime.hour + hours)):
        screen.print_notification("Food consumption should happen now.")

    # TODO: do we need this tick counter if we have the time?
    ticks_elapsed += 1
    current_datetime += timedelta(hours=hours)
    distance_travelled += survivors.car_speed


# This is called every tick of the game
def game_tick():
    if not survivors.survivor_list[0]["alive"]:
        screens.screen_list["dead"]["draw_function"]()

    screens.screen_list["travelling"]["draw_function"]()

    dprint("Start of game tick: " + str(ticks_elapsed))
    dprint("Current date: " + format_date(current_datetime))
    dprint("Current time: " + format_time(current_datetime))

    for event in events:
        event_random = random.uniform(0.0, 100.0)
        if event["occurrence_chance"] > event_random:
            event_function = None

            if event["notification_handler_function"] is not None:
                event_function = event["notification_handler_function"]

            # TODO: Add support for other handler functions that are more complex than a notification

            if event_function is not None:
                notification = event_function()

                if notification is not None:
                    screen.print_notification(notification)

                # NOTE: we don't want more than one event per tick
                break

    for survivor in survivors.survivor_list:
        if survivor["alive"] and survivor["zombified"]:
            random_number = random.randrange(1, 100)

            if random_number <= 50:
                random_survivor = get_random_survivor(True, True, False, False)
                survivor["alive"] = False

                # TODO: subtract a bullet from ammo?
                screen.print_notification(random_survivor["name"] + " managed to shoot a zombified " + survivor["name"] + " dead.")
            elif random_number <= 90:
                random_survivor = get_random_survivor(True, True, False, False)
                random_damage = random.randrange(1, 20)

                random_survivor["health"] -= random_damage

                screen.print_notification("A zombified " + survivor["name"] + " damaged " + random_survivor["name"] + " for " + str(
                    random_damage) + " damage.")
            else:
                if count_survivors(False, False, False, False) > 0:
                    random_survivor = get_random_survivor(False, False, False, False)
                    random_survivor["bitten"] = True

                    screen.print_notification("A zombified " + survivor["name"] + " bit " + random_survivor["name"] + ".")

    for survivor in survivors.survivor_list:
        if survivor["alive"] and survivor["bitten"] and not survivor["zombified"]:
            ticks_since_bitten = survivor["ticks_since_bitten"]

            if ticks_since_bitten > 4:
                if ticks_since_bitten < 24:
                    random_number = random.randrange(1, 100)

                    should_turn = random_number <= ticks_since_bitten * 2
                else:
                    should_turn = True

                if should_turn:
                    survivor["zombified"] = True

                    screen.print_notification(survivor["name"] + " turned into a zombie.")

            survivor["ticks_since_bitten"] = ticks_since_bitten + 1

    next_city = get_next_city(distance_travelled)

    if next_city["distance_from_start"] - distance_travelled <= survivors.car_speed:
        screen.print_notification("You arrived in " + next_city["name"] + "!")

        screens.screen_list["city"]["draw_function"](next_city)
    else:
        dprint("The next city is: " + next_city["name"])

    for survivor in survivors.survivor_list:
        if survivor["alive"] and survivor["health"] <= 0:
            survivor["alive"] = False

            screen.print_notification(survivor["name"] + " died.")

    pass_time(1)


# This is the program entry point
def main():
    screen.init()
    screen.clear()

    # TODO: display a title screen?

    screens.screen_list["starting"]["draw_function"]()

    screens.screen_list["city"]["draw_function"](cities.city_list["Los Angeles"])

    # The main game loop
    while True:
        # Simulate one game tick
        game_tick()

        # NOTE: this may cause weird drawing bugs
        if screens.current_screen is not None and screens.current_screen["name"] != "travelling":
            screens.screen_list["travelling"]["draw_function"]()


# Are we being run as a script? If so, run main().
# '__main__' is the name of the scope in which top-level code executes.
# See https://docs.python.org/3.4/library/__main__.html for explanation
if __name__ == "__main__":
    main()
