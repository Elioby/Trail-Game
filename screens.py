#!/usr/bin/python3

# This file contains data on the screens in the game

import time
import screen
import ascii_helper

from misc_utils import *

# TODO: These are currently useless because of the front buffer, maybe they won't be in future though?
previous_screen = None
current_screen = None


def set_current_screen(new_screen):
    global previous_screen
    global current_screen

    previous_screen = current_screen
    current_screen = new_screen


# TODO: These display functions might work better in their own file
def draw_starting_screen():
    # TODO: Code for the starting screen goes here
    # TODO: This function should not return until they have picked all 4 characters' names
    # TODO: These names should be updated in the survivors list in survivors.py, where survivors[0] is the main player

    # TODO: use the input function to ask for the players name, and for three other friends they can count on eg: input("What is your name? ")

    # TODO: update the names in survivors.py by using the survivors list eg: survivors[0] = player_name

    screen.clear()

    set_current_screen(screen_list["starting"])

    print("This is the starting screen")

    wait_key()


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


def draw_travelling_screen():
    set_current_screen(screen_list["travelling"])

    car_body_image = ascii_helper.load_image("resources/car_body.ascii")
    car_wheel_image_1 = ascii_helper.load_image("resources/car_wheel_1.ascii")
    car_wheel_image_2 = ascii_helper.load_image("resources/car_wheel_2.ascii")

    # TODO: this is kinda messy
    iterations = 0
    wheel = 0
    road = 0

    while True:
        screen.draw_ascii_image(1, 1, car_body_image)

        if wheel == 0:
            screen.draw_ascii_image(15, 8, car_wheel_image_2)
            screen.draw_ascii_image(54, 8, car_wheel_image_2)
        else:
            screen.draw_ascii_image(15, 8, car_wheel_image_1)
            screen.draw_ascii_image(54, 8, car_wheel_image_1)

        for x in range(car_body_image["width"] + 1):
            pixel_char = "="

            if road < 1:
                if x % 2 == 0:
                    pixel_char = "-"
            else:
                if x % 2 != 0:
                    pixel_char = "-"

            screen.draw_pixel(x, 11, pixel_char)

        screen.flush()

        wheel += 0.25
        road += 1

        if wheel > 1:
            iterations += 1

            if iterations > 3:
                return

        if road > 1:
            road = 0

        time.sleep(0.25)


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

    "travelling": {
        "name": "travelling",

        "draw_function": draw_travelling_screen
    },
}
