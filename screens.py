#!/usr/bin/python3
# coding=utf-8

# This file contains data on the screens in the game

import game
import time
import screen
import survivors
import ascii_helper

from misc_utils import *
from datetime import timedelta

# TODO: These are currently useless because of the front buffer, maybe they won't be in future though?
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

    screen.clear()

    set_current_screen(screen_list["starting"])

    print("This is the starting screen")

    screen.wait_key()


def draw_dead_screen():
    # TODO: Code for the dead screen goes here
    # TODO: This function should never return (use quit() ? unless that's a bad idea for some reason)

    # TODO: Replace with something else

    screen.clear()
    set_current_screen(screen_list["dead"])

    print("You died!")

    quit()


def draw_city_screen(city):
    # TODO: Code for the city screen goes here
    # TODO: This function should not return until they leave the city

    # TODO: Replace with something else

    screen.clear()
    set_current_screen(screen_list["city"])

    ignored_input = input("You are in " + city["name"] + ", what would you like to do? ")


def draw_trading_screen():
    # TODO: Code for the trading screen goes here

    # TODO: Replace with something else
    screen.clear()

    print("This is the trading screen")

    screen.wait_key()


def draw_resting_screen():
    # TODO: Code for the resting screen goes here

    # TODO: Replace with something else
    screen.clear()

    print("This is the resting screen")

    screen.wait_key()


def draw_put_down_screen():
    # TODO: Code for the put down screen goes here

    # TODO: Replace with something else
    screen.clear()

    print("This is the put down screen")

    screen.wait_key()


def draw_travelling_screen():
    set_current_screen(screen_list["travelling"])

    car_body_image = ascii_helper.load_image("resources/car_body.ascii")
    car_wheel_image_1 = ascii_helper.load_image("resources/car_wheel_1.ascii")
    car_wheel_image_2 = ascii_helper.load_image("resources/car_wheel_2.ascii")

    car_x = int((screen.get_width() / 2) - (car_body_image["width"] / 2))
    car_y = int((screen.get_height() / 2) - car_body_image["height"])

    # TODO: this is kinda messy
    iterations = 0
    wheel = 0
    road = 0

    while True:
        # Draw survivors stats
        survivor_y = 0

        health_x = 0

        for survivor in survivors.survivor_list:
            survivor_name = survivor["name"]
            survivor_name_length = len(survivor_name)

            if survivor_name_length > health_x:
                health_x = survivor_name_length

            screen.draw_text(1, survivor_y + 1, survivor_name)

            survivor_y += 2

        survivor_y = 0

        total_bars = 14

        for survivor in survivors.survivor_list:
            if survivor["alive"]:
                remaining_bars = int(max((survivor["health"] / survivor["max_health"]) * total_bars, 1))

                screen.draw_text(health_x + 3, survivor_y + 1, "[" + ("█" * remaining_bars) + (" " * (total_bars - remaining_bars)) + "]")

                if survivor["zombified"]:
                    screen.draw_text(health_x + total_bars + 6, survivor_y + 1, "(ZOMBIE)")
                elif survivor["bitten"]:
                    screen.draw_text(health_x + total_bars + 6, survivor_y + 1, "(BITTEN)")
            else:
                padding = int((total_bars - 4) / 2)
                screen.draw_text(health_x + 3, survivor_y + 1, "[" + (padding * " ") + "DEAD" + (padding * " ") + "]")

            survivor_y += 2

        # Draw datetime

        screen.draw_text(health_x + 30, 1, format_time(survivors.current_datetime))
        screen.draw_text(health_x + 30, 3, format_date(survivors.current_datetime))

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

        wheel += 0.25
        road += 1

        if wheel > 1:
            iterations += 1

            if iterations > 2:
                return

        if road > 1:
            road = 0

        time.sleep(0.15)


def draw_win_screen():
    # TODO: Code for the dead screen goes here
    # TODO: This function should never return (use quit() ? unless that's a bad idea for some reason)

    # TODO: Replace with something else

    screen.clear()
    set_current_screen(screen_list["win"])

    print("You made it to New York! You win!")

    quit()


screen_list = {
    "starting": {
        "name": "starting",

        "draw_function": draw_starting_screen
    },

    "dead": {
        "name": "dead",

        "draw_function": draw_dead_screen
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

    "win": {
        "name": "win",

        "draw_function": draw_win_screen
    },
}