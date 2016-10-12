#!/usr/bin/python3

# This file contains functions to help you operate the screen, such as clearing, drawing and flushing
# 	This is only for complex screens like the traveling screen, for other screens, use the print and input functions 

import os
import pip
import sys
import math
import time
import shutil
import subprocess

from misc_utils import *

should_restart = False

try:
    import numpy
except ImportError:
    print("ERROR: Importing numpy failed, installing and restarting now..")
    pip.main(['install', 'numpy', '--user'])
    should_restart = True

try:
    from colorama import init

    init()
except ImportError:
    print("ERROR: Importing colorama failed, installing and restarting now..")
    pip.main(['install', 'colorama', '--user'])
    should_restart = True

if should_restart:
    subprocess.call(['python', 'game.py'])
    quit()

width = 0
height = 0

# Holds "pixel" data on the currently shown screen
front_buffer = None

# Holds "pixel" data on the currently rendering and next to be shown screen
back_buffer = None


def init():
    global front_buffer
    global back_buffer
    global width
    global height

    width = shutil.get_terminal_size()[0] - 1
    height = shutil.get_terminal_size()[1] - 1

    front_buffer = numpy.chararray((width, height))
    back_buffer = numpy.chararray((width, height))

    front_buffer.fill("")
    back_buffer.fill("")


def clear():
    os.system("cls")


def get_width():
    return width


def get_height():
    return height


def draw_rect(rect_x, rect_y, rect_width, rect_height):
    min_x = max(rect_x, 0)
    max_x = min(rect_x + rect_width, width)

    min_y = max(rect_y, 0)
    max_y = min(rect_y + rect_height, height)

    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            back_buffer[x][y] = "#"


def draw_ascii_image(image_x, image_y, ascii_image):
    image_buffer = ascii_image["image_buffer"]
    image_width = ascii_image["width"]
    image_height = ascii_image["height"]

    min_x = max(image_x, 0)
    max_x = min(image_x + image_width, width)

    min_y = max(image_y, 0)
    max_y = min(image_y + image_height, height)

    image_x = 0
    image_y = 0

    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            back_buffer[x][y] = image_buffer[image_x][image_y]

            image_y += 1

        image_y = 0
        image_x += 1


def draw_pixel(pixel_x, pixel_y, pixel_char):
    back_buffer[pixel_x][pixel_y] = pixel_char


# NOTE: this function does not use the front or back buffer as we want the front buffer to stay intact, this is why it's called print instead of draw
def print_notification(message):
    message_length = len(message)

    x_start = (width / 2) - (message_length / 2)
    y_start = (height / 2)

    set_cursor(x_start - 3, y_start - 2)

    sys.stdout.write("╔" + "═" * (message_length + 4) + "╗")

    set_cursor(x_start - 2, y_start - 1)

    sys.stdout.write(" " * (message_length + 4))

    set_cursor(x_start, y_start)

    sys.stdout.write(message)

    set_cursor(x_start - 2, y_start + 1)

    sys.stdout.write(" " * (message_length + 4))

    for j in range(-1, 2):
        set_cursor(x_start - 3, y_start + j)
        sys.stdout.write("║")

    for j in range(-1, 2):
        set_cursor(x_start + message_length + 2, y_start + j)
        sys.stdout.write("║")

    set_cursor(x_start - 2, y_start)
    sys.stdout.write(" " * 2)

    set_cursor(x_start + message_length, y_start)
    sys.stdout.write(" " * 2)

    set_cursor(x_start - 3, y_start + 2)

    sys.stdout.write("╚" + "═" * (message_length + 4) + "╝")

    set_cursor(1, 1)

    wait_key()

    refresh()


def set_cursor(cursor_x, cursor_y):
    sys.stdout.write("\033[" + str(max(int(cursor_y), 0)) + ";" + str(max(int(cursor_x), 0)) + "H")


# Re-renders the front buffer to the screen
def refresh():
    render_buffer(front_buffer)


def flush():
    render_buffer(back_buffer)

    numpy.copyto(front_buffer, back_buffer)

    back_buffer.fill("")


def render_buffer(buffer_to_render):
    clear()

    for col in buffer_to_render.T:
        content = ""
        for cell in col:
            cell_string = str(cell)[2:3]
            if cell_string != "":
                content += cell_string
            else:
                content += " "

        print(content)
