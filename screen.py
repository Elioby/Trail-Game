#!/usr/bin/python3

# This file contains functions to help you operate the screen, such as clearing, drawing and flushing
# 	This is only for complex screens like the traveling screen, for other screens, use the print and input functions 

import os
import pip
import ctypes
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
    from colorama import init, win32

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

# These variables are used to optimise printing the buffer by skipping with the cursor to the start, and finishing before the end
buffer_start = {"x": None, "y": None}
buffer_end = {"x": 0, "y": 0}


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
    if platform.system() == "Windows":
        console_buffer_info = win32.GetConsoleScreenBufferInfo(win32.STDOUT)
        cells_in_screen = console_buffer_info.dwSize.X * console_buffer_info.dwSize.Y

        win32.FillConsoleOutputCharacter(win32.STDOUT, ' ', cells_in_screen, win32.COORD(0, 0))
        set_cursor(1, 1)
    else:
        os.system("clear")


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
            draw_pixel(x, y, image_buffer[image_x][image_y])

            image_y += 1

        image_y = 0
        image_x += 1


def draw_pixel(pixel_x, pixel_y, pixel_char):
    if pixel_char != "" and pixel_char != " ":
        if buffer_start["y"] is None or pixel_y < buffer_start["y"]:
            buffer_start["y"] = pixel_y

        if buffer_end["y"] is None or pixel_y > buffer_end["y"]:
            buffer_end["y"] = pixel_y

    if pixel_x >= width or pixel_y >= height:
        return

    back_buffer[pixel_x][pixel_y] = pixel_char


def draw_text(text_x, text_y, text):
    text_length = len(text)

    for x in range(text_length):
        draw_pixel(x + text_x, text_y, text[x])


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
    win32.SetConsoleCursorPosition(win32.STDOUT, (max(int(cursor_y), 1), max(int(cursor_x), 1)))


# Re-renders the front buffer to the screen
def refresh():
    render_buffer(front_buffer)


def flush():
    render_buffer(back_buffer)

    numpy.copyto(front_buffer, back_buffer)

    back_buffer.fill("")


def render_buffer(buffer_to_render):




    if platform.system() == "Windows":
        # Win32API structs
        class SMALL_RECT(ctypes.Structure):
            _fields_ = ('left', ctypes.c_short), ('top', ctypes.c_short), ('right', ctypes.c_short), ('bottom', ctypes.c_short)


        class COORD(ctypes.Structure):
            _fields_ = ('x', ctypes.c_short), ('y', ctypes.c_short)


        class CHAR_INFO(ctypes.Structure):
            _fields_ = ('ascii', ctypes.c_char), ('attr', ctypes.c_uint16)

        buf = (CHAR_INFO * (width * height))()

        x = 0
        y = 0

        for c in buf:
            pixel = buffer_to_render[x][y]

            if pixel == "":
                pixel = b" "

            c.ascii = pixel
            c.attr = 7

            x += 1

            if x >= width:
                x = 0
                y += 1

        console_handle = ctypes.windll.kernel32.CreateFileA(
            ctypes.create_string_buffer(b"CONOUT$"),
            0x40000000 | 0x80000000,  # Generic read and write permissions
            1 | 2,  # We want read and write permissions
            0,
            3,  # Open the file only if it exists
            0,
            0)

        if console_handle == 0:
            raise ctypes.WinError()

        if ctypes.windll.kernel32.WriteConsoleOutputA(console_handle, ctypes.byref(buf), COORD(width, height), COORD(0, 0), ctypes.byref(SMALL_RECT(0, 0, width - 1, height - 1))) == 0:
            raise ctypes.WinError()
    else:
        clear()

        start_x = buffer_start["x"]
        start_y = buffer_start["y"]

        end_x = buffer_end["x"]
        end_y = buffer_end["y"]

        if start_x is None:
            start_x = 1

        if start_y is None:
            start_y = 1

        if end_x is None:
            end_x = 1

        if end_y is None:
            end_y = 1

        set_cursor(start_x, start_y)

        y = 0
        for col in buffer_to_render.T:
            y += 1

            if y < start_y:
                continue

            content = ""
            for cell in col:
                cell_string = str(cell)[2:3]
                if cell_string != "":
                    content += cell_string
                else:
                    content += " "

            print(content)

            if y > end_y:
                break
