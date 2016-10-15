#!/usr/bin/python3
# coding=utf-8

# This file contains data on the screens in the game

import time

import ascii_helper
import screen
from misc_utils import *

previous_screen = None
current_screen = None


def set_current_screen(new_screen):
    global previous_screen
    global current_screen

    previous_screen = current_screen
    current_screen = new_screen


def draw_starting_screen():
    # TODO: Code for the starting screen goes here
    # TODO: This function should not return until they have picked all 4 characters' names
    # TODO: These names should be updated in the survivors list in survivors.py, where survivors[0] is the main player

    # TODO: use the input function to ask for the players name, and for three other friends they can count on eg: input("What is your name? ")

    # TODO: update the names in survivors.py by using the survivors list eg: survivors[0] = player_name

    # TODO: enforce names so that they are not longer than 16 characters

    # TODO: the player should be informed about what they start with, how much food, how many medkits, how much money

    screen.clear()

    set_current_screen(screen_list["starting"])

    print("This is the starting screen")

    screen.wait_key()


def draw_dead_screen():
    screen.clear()
    set_current_screen(screen_list["dead"])

    game_over_image = ascii_helper.load_image("resources/dead_game_over.ascii")
    tombstone_image = ascii_helper.load_image("resources/dead_tombstone.ascii")

    game_over_x = int((screen.get_width() / 2) - (game_over_image["width"] / 2)) - 1
    tombstone_x = int((screen.get_width() / 2) - (tombstone_image["width"] / 2))

    screen.draw_ascii_image(game_over_x, 0, game_over_image)
    screen.draw_ascii_image(tombstone_x, game_over_image["height"] + 2, tombstone_image)

    screen.flush()

    time.sleep(2)

    screen.print_notification("Press any key to continue.", False)

    draw_points_screen()


def draw_win_screen():
    # TODO: Code for the dead screen goes here
    # TODO: This function should never return (use quit() ? unless that's a bad idea for some reason)

    screen.clear()
    set_current_screen(screen_list["win"])

    # TODO: Replace with something else

    print("You made it to New York! You win!")

    draw_points_screen()


# TODO: this needs some prettifying
def draw_points_screen():
    screen.clear()

    set_current_screen(screen_list["points"])

    points = 0

    points += survivors.distance_travelled

    points += count_survivors(True, False, False, False) * 250

    print("Total score: " + str(points) + ".")

    time.sleep(2)

    screen.print_notification("Press any key to exit.", False)

    screen.clear()

    quit()


def draw_city_screen(city):
    set_current_screen(screen_list["city"])

    while True:
        screen.clear()
        print("You enter the city of " + city["name"])

        # Show options to player:
        print("You can:")
        print("1: Get information on " + city["name"] + ".")
        print("2: Check survivors status.")
        print("3: Trade with other survivors.")
        print("4: Go to the bar.")
        print("5: Rest.")
        print("6: Move on to " + get_next_city(survivors.distance_travelled + survivors.car_speed)["name"] + ".")
        print("")
        player_choice = input("What would you like to do? ")

        # Evaluate the players decision:
        player_choice = normalise_input(player_choice)
        if player_choice == "1":
            screen.clear()
            # Get information
            print("You are in " + city["name"] + ".")
            print(city["description"])
            # TODO: Maybe information on whats available, like traders, inns to stay, etc...?
            print("The next city is " + get_next_city(survivors.distance_travelled + survivors.car_speed)["name"] + ".")

            # Return to options
            input("Press enter to go back...")
        elif player_choice == "2":
            # Check status
            draw_put_down_screen()
        elif player_choice == "3":
            # Trade
            draw_trading_screen()
        elif player_choice == "4":
            # Bar
            pass
        elif player_choice == "5":
            # Rest
            draw_resting_screen()
        elif player_choice == "6":
            # Continue to travelling screen
            return
        # TODO: Remove after debugged
        elif player_choice == "7":
            # Debugging for dead screen
            draw_dead_screen()
        else:
            # Invalid input
            print("Please enter a number between 1 and 6.")


def draw_trading_screen():
    # TODO: Code for the trading screen goes here

    # TODO: Replace with something else
    screen.clear()

    survivors_items_count = len(survivors.group_inventory)

    if survivors_items_count <= 0 and survivors.group_money <= 0:
        print("You have nothing to trade.")
        time.sleep(2)
        return

    trades = {}

    for i in range(3):
        # None means use money
        survivors_item = None

        # If they have more than 0 items, and they either don't have money or a 60% chance, use random item - otherwise use money for this trade
        if survivors_items_count > 0 and (survivors.group_money <= 0 or random.randrange(1, 100) <= 60):
            # Get a random item from the group inventory
            survivors_item = get_random_dict_value(survivors.group_inventory)

        if survivors_item is not None:
            print("Use item " + str(survivors_item))
        else:
            print("Use money")

    if len(trades) == 0:
        print("You have nothing to trade.")
        time.sleep(2)
        return

    screen.wait_key()


def draw_resting_screen():
    # TODO: Code for the resting screen goes here

    # TODO: Replace with something else
    screen.clear()

    print("This is the resting screen")

    screen.wait_key()


def draw_put_down_screen():
    set_current_screen(screen_list["put_down"])
    screen.clear()
    # Display the survivors status

    # Players information:
    if not survivors.survivor_list[0]["bitten"]:
        print("Your health is " + str(survivors.survivor_list[0]["health"]) + ".")
    else:
        print("Your health is " + str(survivors.survivor_list[0]["health"]) + ", and you have been bitten.")

    # Other survivors information:
    for survivor in survivors.survivor_list:
        if survivor["alive"] and not survivor["bitten"]:
            print(survivor["name"] + " has " + str(survivor["health"]) + " health.")
        elif survivor["alive"] and survivor["bitten"] and not survivor["zombified"]:
            print(survivor["name"] + " has " + str(survivor["health"]) + " health, and has been bitten")
        elif not survivor["alive"]:
            print(survivor["name"] + " is dead.")

    print("")

    # Display options
    while True:
        option_count = 2
        options_available = {}

        print("1: Go back")
        print("2: Commit suicide")

        for i in range(1, len(survivors.survivor_list)):
            if survivor["alive"]:
                option_count += 1
                options_available.update({option_count: i})
                print(str(option_count) + ": Put down " + str(survivor["name"]) + ".")

        # Evaluate users input:
        user_choice = input("What would you like to do? ")

        try:
            user_choice = int(user_choice)
        except ValueError:
            print("Please enter a number.")
            continue

        if user_choice == 1:
            # Return to city menu screen
            draw_city_screen(get_next_city(survivors.distance_travelled))
        elif user_choice == 2:
            # Suicide
            draw_dead_screen()
        elif user_choice <= option_count:
            # Search through options available to find who to kill
            survivors.survivor_list[options_available[user_choice]]["alive"] = False
            print("You killed " + survivors.survivor_list[options_available[user_choice]]["name"])
        else:
            print("Please enter a number between 1 and " + str(option_count) + ".")


def draw_travelling_screen():
    show_next_city_notification = current_screen["name"] == "city"

    set_current_screen(screen_list["travelling"])

    car_body_image = ascii_helper.load_image("resources/car_body.ascii")
    car_wheel_image_1 = ascii_helper.load_image("resources/car_wheel_1.ascii")
    car_wheel_image_2 = ascii_helper.load_image("resources/car_wheel_2.ascii")

    survivor_x_start = int(screen.get_width() / 10)
    survivor_y_start = screen.get_height() - (len(survivors.survivor_list) * 2) - 1

    car_x = int((screen.get_width() / 2) - (car_body_image["width"] / 2))
    car_y = survivor_y_start - car_body_image["height"] - 5

    # TODO: This is kinda messy
    iterations = 0
    wheel = 0
    road = 0

    while True:
        # Draw travelling progress bar
        progress_bar_box_width = int(screen.get_width() / 1.5)
        progress_bar_box_x = int((screen.get_width() / 2) - (progress_bar_box_width / 2))

        progress_bar_width = progress_bar_box_width - 6

        screen.draw_bordered_rect(progress_bar_box_x, -1, progress_bar_box_width, 5)

        screen.draw_pixel(int(progress_bar_box_x + 2), 1, "|")
        screen.draw_pixel(int(progress_bar_box_x + progress_bar_width + 3), 1, "|")

        for x in range(progress_bar_box_x + 3, progress_bar_box_x + progress_bar_box_width - 3):
            screen.draw_pixel(x, 1, "-")

        progress_bar_current_x = progress_bar_box_x + 3 + (
        (survivors.distance_travelled / get_end_distance()) * progress_bar_width)

        screen.draw_pixel(int(progress_bar_current_x), 2, "^")

        # Draw survivors stats
        survivor_y = survivor_y_start

        health_x = 0

        for survivor in survivors.survivor_list:
            survivor_name = survivor["name"]
            survivor_name_length = len(survivor_name)

            if survivor_name_length > health_x:
                health_x = survivor_name_length

            screen.draw_text(survivor_x_start, survivor_y + 1, survivor_name)

            survivor_y += 2

        survivor_y = survivor_y_start + 1

        total_bars = 14

        for survivor in survivors.survivor_list:
            if survivor["alive"]:
                screen.draw_progress_bar(survivor_x_start + health_x + 2, survivor_y, total_bars,
                                         survivor["health"] / survivor["max_health"])

                if survivor["zombified"]:
                    screen.draw_text(survivor_x_start + health_x + total_bars + 6, survivor_y + 1, "(ZOMBIE)")
                elif survivor["bitten"]:
                    screen.draw_text(survivor_x_start + health_x + total_bars + 6, survivor_y + 1, "(BITTEN)")
            else:
                padding = int((total_bars - 4) / 2)
                screen.draw_text(survivor_x_start + health_x + 3, survivor_y + 1,
                                 "[" + (padding * " ") + "DEAD" + (padding * " ") + "]")

            survivor_y += 2

        # Draw stats
        next_city = get_next_city(survivors.distance_travelled)

        stat_lines = ["Time: " + format_time(survivors.current_datetime),
                      "Date: " + format_date(survivors.current_datetime),
                      "Next City: " + next_city["name"], "Distance: " + str(
                int(next_city["distance_from_start"] - survivors.distance_travelled)) + " miles"]

        longest_line = 0

        for stat_line in stat_lines:
            stat_line_length = len(stat_line)
            if stat_line_length > longest_line:
                longest_line = stat_line_length

        stat_x = int(screen.get_width() - longest_line - (screen.get_width() / 10) + 2)
        stat_y = survivor_y_start + 1

        for stat_line in stat_lines:
            screen.draw_text(stat_x, stat_y, stat_line)

            stat_y += 2

        # Draw the car
        screen.draw_ascii_image(car_x, car_y, car_body_image)

        if wheel <= 0.25:
            screen.draw_ascii_image(car_x + 14, car_y + 7, car_wheel_image_2)
            screen.draw_ascii_image(car_x + 53, car_y + 7, car_wheel_image_2)
        else:
            screen.draw_ascii_image(car_x + 14, car_y + 7, car_wheel_image_1)
            screen.draw_ascii_image(car_x + 53, car_y + 7, car_wheel_image_1)

        for x in range(screen.get_width()):
            pixel_char = "="

            if road < 1:
                if x % 2 == 0:
                    pixel_char = "-"
            else:
                if x % 2 != 0:
                    pixel_char = "-"

            screen.draw_pixel(x, car_y + car_body_image["height"] + 2, pixel_char)

        screen.flush()

        if show_next_city_notification:
            next_city = get_next_city(survivors.distance_travelled)
            screen.print_notification(next_city["name"] + " is " + str(
                int(next_city["distance_from_start"] - survivors.distance_travelled)) + " miles away.")
            show_next_city_notification = False

        wheel += 0.25
        road += 1

        if wheel > 1:
            iterations += 1

            if iterations > 2:
                return

        if road > 1:
            road = 0

        time.sleep(0.15)


screen_list = {
    "starting": {
        "name": "starting",

        "draw_function": draw_starting_screen
    },

    "dead": {
        "name": "dead",

        "draw_function": draw_dead_screen
    },

    "win": {
        "name": "win",

        "draw_function": draw_win_screen
    },

    "points": {
        "name": "points",

        "draw_function": draw_points_screen
    },

    "city": {
        "name": "city",

        "draw_function": draw_city_screen
    },

    "trading": {
        "name": "trading",

        "draw_function": draw_trading_screen
    },

    "resting": {
        "name": "resting",

        "draw_function": draw_resting_screen
    },

    "put_down": {
        "name": "put_down",

        "draw_function": draw_put_down_screen
    },

    "travelling": {
        "name": "travelling",

        "draw_function": draw_travelling_screen
    },
}
