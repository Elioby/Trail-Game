#!/usr/bin/python3
# coding=utf-8

# This file contains functions to help you operate the screen, such as clearing, drawing and flushing
# 	This is only for complex screens like the traveling screen, for other screens, use the print and input functions 

import os
import pip
import sys
import ctypes
import shutil
import platform
import subprocess
import ascii_helper

if platform.system() == "Windows":
    import win32_structs

try:
    import numpy
except ImportError:
    print("ERROR: Importing numpy failed, installing and restarting now..")
    pip.main(['install', 'numpy', '--user'])
    subprocess.call(['python', 'game.py'])
    quit()

stdout = None

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
    global stdout
    global front_buffer
    global back_buffer
    global width
    global height

    # Get the handle of the console's standard output (stdout)
    if platform.system() == "Windows":
        stdout = ctypes.windll.kernel32.GetStdHandle(-11)

    width = shutil.get_terminal_size()[0] - 1
    height = shutil.get_terminal_size()[1] - 1

    front_buffer = numpy.chararray((width, height))
    back_buffer = numpy.chararray((width, height))

    front_buffer.fill("")
    back_buffer.fill("")


def set_cursor_visibility(visible):
    if platform.system() == "Windows":
        cursor_info = win32_structs.CONSOLE_CURSOR_INFO()

        ctypes.windll.kernel32.GetConsoleCursorInfo(stdout, ctypes.byref(cursor_info))

        cursor_info.visible = visible

        ctypes.windll.kernel32.SetConsoleCursorInfo(stdout, ctypes.byref(cursor_info))
    else:
        if visible:
            print("\e[?25h")
        else:
            print("\e[?25l")


def wait_key():
    result = None
    if platform.system() == "Windows":
        import msvcrt
        result = msvcrt.getch()
    else:
        import termios
        fd = sys.stdin.fileno()

        old_term = termios.tcgetattr(fd)
        new_attr = termios.tcgetattr(fd)
        new_attr[3] = new_attr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, new_attr)

        try:
            result = sys.stdin.read(1)
        except IOError:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)

    return result


def clear():
    if platform.system() == "Windows":
        os.system("cls")
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


def draw_bordered_rect(rect_x, rect_y, rect_width, rect_height, fill_char=" "):
    for x in range(rect_x + 1, rect_x + rect_width - 1):
        draw_pixel(x, rect_y, "═")

    for x in range(rect_x + 1, rect_x + rect_width - 1):
        draw_pixel(x, rect_y + rect_height - 1, "═")

    for y in range(rect_y + 1, rect_y + rect_height - 1):
        draw_pixel(rect_x, y, "║")

    for y in range(rect_y + 1, rect_y + rect_height - 1):
        draw_pixel(rect_x + rect_width - 1, y, "║")

    draw_pixel(rect_x, rect_y, "╔")
    draw_pixel(rect_x + rect_width - 1, rect_y, "╗")
    draw_pixel(rect_x, rect_y + rect_height - 1, "╚")
    draw_pixel(rect_x + rect_width - 1, rect_y + rect_height - 1, "╝")

    if fill_char is not None:
        for x in range(rect_x + 1, rect_x + rect_width - 1):
            for y in range(rect_y + 1, rect_y + rect_height - 1):
                draw_pixel(x, y, fill_char)


def draw_progress_bar(bar_x, bar_y, length, progress):
    remaining_bars = int(max(progress * length, 1))

    draw_text(bar_x, bar_y, "[" + ("█" * remaining_bars) + (" " * (length - remaining_bars)) + "]")


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


def get_decision_input(decisions, selected_index=1):
    decisions_count = len(decisions)

    key = wait_key()

    if key == b"\r":
        return selected_index, True
    elif key == b"\xe0":
        key = wait_key()
        key_ordinal = ord(key)

        if key_ordinal == 80:
            selected_index += 1
        elif key_ordinal == 72:
            selected_index -= 1

    if selected_index > decisions_count:
        selected_index = decisions_count
    elif selected_index < 1:
        selected_index = 1

    return selected_index, False


def draw_decision(decision_x, decision_y, decisions, selected_index=1):
    decisions_count = len(decisions)

    for i in range(decisions_count):
        decision = decisions[i]

        y = decision_y + (i * 2)

        text_length = len(decision)

        x = decision_x

        if decision_x is None:
            x = int((get_width() / 2) - ((text_length + 3) / 2))

        draw_text(x + 2, y, decision)

        if selected_index == i + 1:
            draw_text(x, y, ">")
            draw_text(x + text_length + 3, y, "<")


# NOTE: (docs) this flushes the display for you (probably shouldn't)
def draw_decision_box(body_text, decisions, selected_index=1, decision_x=None, decision_y=None, max_width=None, max_height=None):
    box_width = int(get_width() - get_width() / 6)
    box_height = int(get_height() - get_height() / 6)

    if max_width is not None:
        box_width = min(box_width, max_width)

    if max_height is not None:
        box_height = min(box_height, max_height)

    if decision_x is None:
        decision_x = int((get_width() / 2) - (box_width / 2))

    if decision_y is None:
        decision_y = int((get_height() / 2) - (box_height / 2))

    draw_bordered_rect(decision_x, decision_y, box_width, box_height, " ")
    lines = draw_text_wrapped(decision_x + 6, decision_y + 3, body_text, box_width - 1, False)

    draw_decision(decision_x + 5, decision_y + lines + 6, decisions, selected_index)

    return decision_x, decision_y


def draw_pixel(pixel_x, pixel_y, pixel_char):
    if pixel_char != "" and pixel_char != " ":
        if buffer_start["y"] is None or pixel_y < buffer_start["y"]:
            buffer_start["y"] = pixel_y

        if buffer_end["y"] is None or pixel_y > buffer_end["y"]:
            buffer_end["y"] = pixel_y

    if pixel_x >= width or pixel_x < 0 or pixel_y >= height or pixel_y < 0:
        return

    try:
        back_buffer[pixel_x][pixel_y] = pixel_char
    except UnicodeEncodeError:
        back_buffer[pixel_x][pixel_y] = str(pixel_char).encode(sys.stdout.encoding)


# TODO: (Add docs) returns the amount of vertical lines it used
def draw_text_wrapped(text_x, text_y, text, max_length, indent=False):
    words = text.split(" ")

    x = text_x
    y = text_y

    for word in words:
        word_length = len(word)

        if x + word_length > max_length:
            x = text_x

            if indent:
                x += 2

            y += 1

        for i in range(word_length):
            char = word[i]

            if char is "\n":
                y += 1
                x = text_x

                if indent:
                    x += 2

                continue
            else:
                draw_pixel(x, y, char)

            if x > max_length:
                x = text_x

                if indent:
                    x += 2

                y += 1

            x += 1

        x += 1

    return y - text_y


def draw_text(text_x, text_y, text):
    text = text
    text_length = len(text)

    for x in range(text_length):
        draw_pixel(x + text_x, text_y, text[x])


def draw_ascii_numbers(x, y, input_number):
    ascii_numbers = []
    x_spacing = 2
    x_offset = 0
    input_number = str(input_number)

    for i in range(0, 9):
        ascii_numbers.append(ascii_helper.load_image("resources/numbers/" + str(i) + ".ascii"))

    for i in range(0, len(input_number)):
        num = int(input_number[i])
        draw_ascii_image(x + x_offset, y, ascii_numbers[num])
        x_offset += ascii_numbers[num]["width"] + x_spacing


def draw_ascii_font_text(text_x, text_y, text, font):
    last_width = 0

    for char in text:
        text_x += last_width
        char_code = ord(char)
        char_start = ((char_code - 32) * font["height"])

        last_width = 0

        for i in range(font["height"]):
            line = font["font_data"][char_start + i + 1]
            line_length = len(line)

            if line_length > last_width:
                last_width = line_length - 2

            char_x = text_x

            for x in line:
                if x != "@":
                    if x == font["hardblank_character"]:
                        draw_pixel(char_x, text_y + i, " ")
                    else:
                        draw_pixel(char_x, text_y + i, x)
                else:
                    if i + 1 >= font["height"]:
                        break
                char_x += 1


# NOTE: this function does not use the front or back buffer as we want the front buffer to stay intact, this is why it's called print instead of draw
def print_notification(message, redraw_on_exit=True):
    set_cursor_visibility(False)
    message_length = len(message)

    x_start = (width / 2) - (message_length / 2)
    y_start = (height / 2)

    set_cursor_position(x_start - 3, y_start - 2)

    stdout_write_flush("╔" + "═" * (message_length + 4) + "╗")

    set_cursor_position(x_start - 2, y_start - 1)

    stdout_write_flush(" " * (message_length + 4))

    set_cursor_position(x_start, y_start)

    stdout_write_flush(message)

    set_cursor_position(x_start - 2, y_start + 1)

    stdout_write_flush(" " * (message_length + 4))

    for j in range(-1, 2):
        set_cursor_position(x_start - 3, y_start + j)
        stdout_write_flush("║")

    for j in range(-1, 2):
        set_cursor_position(x_start + message_length + 2, y_start + j)
        stdout_write_flush("║")

    set_cursor_position(x_start - 2, y_start)
    stdout_write_flush(" " * 2)

    set_cursor_position(x_start + message_length, y_start)
    stdout_write_flush(" " * 2)

    set_cursor_position(x_start - 3, y_start + 2)

    stdout_write_flush("╚" + "═" * (message_length + 4) + "╝")

    set_cursor_position(0, 0)

    wait_key()

    if redraw_on_exit:
        refresh()

    set_cursor_visibility(True)


def stdout_write_flush(message):
    sys.stdout.write(message)
    sys.stdout.flush()


def set_cursor_position(cursor_x, cursor_y):
    if platform.system() == "Windows":
        adjusted_position = win32_structs.COORD(int(cursor_x), int(cursor_y))

        ctypes.windll.kernel32.SetConsoleCursorPosition(stdout, adjusted_position)
    else:
        stdout_write_flush("\033[" + str(int(cursor_y) + 1) + ";" + str(int(cursor_x) + 1) + "H")


# Re-renders the front buffer to the screen
def refresh():
    render_buffer(front_buffer)


def flush():
    render_buffer(back_buffer)

    numpy.copyto(front_buffer, back_buffer)

    back_buffer.fill("")


def render_buffer(buffer_to_render):
    if platform.system() == "Windows":
        buf = (win32_structs.CHAR_INFO * (width * height))()

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
            3,  # Open the "file" only if it exists
            0,
            0)

        if console_handle == 0:
            raise ctypes.WinError()

        if ctypes.windll.kernel32.WriteConsoleOutputA(console_handle, ctypes.byref(buf), win32_structs.COORD(width, height),
                                                      win32_structs.COORD(0, 0),
                                                      ctypes.byref(win32_structs.SMALL_RECT(0, 0, width, height))) == 0:
            raise ctypes.WinError()

        # NOTE: Always remember to close your handles!
        ctypes.windll.kernel32.CloseHandle(console_handle)
    else:
        clear()

        start_x = buffer_start["x"]
        start_y = buffer_start["y"]

        end_y = buffer_end["y"]

        if start_x is None:
            start_x = 1

        if start_y is None:
            start_y = 1

        if end_y is None:
            end_y = 1

        set_cursor_position(start_x, start_y)

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
        pass


