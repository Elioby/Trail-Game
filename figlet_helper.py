#!/usr/bin/python3
# coding=utf-8

# This file contains functions to parse figlet fonts (.flf files)

font_cache = {}


def load_font(filename):
    if filename in font_cache:
        return font_cache[filename]

    file = open(filename, "rb")

    data = file.read()
    data = data.decode("utf-8", "replace")

    sections = data.splitlines()

    header = sections[0]

    if header[:5] != "flf2a":
        print("ERROR: File at \"" + filename + "\" is not in the figlet format.")
        return None

    hardblank_character = header[5]

    header_numbers = header[7:].split(" ")

    height, base_line, max_length, old_layout, comment_lines = map(int, header_numbers[:5])

    font = {"hardblank_character": hardblank_character, "height": height, "font_data": sections[height + 2:]}

    font_cache[filename] = font

    return font
