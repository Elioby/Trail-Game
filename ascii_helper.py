#!/usr/bin/python3

# This file contains functions for reading, processing and altering ascii art

import pip

try:
    import numpy
except ImportError:
    print("ERROR: Importing numpy failed, installing and restarting now..")
    pip.main(['install', 'numpy', '--user'])
    should_restart = True

from debug import *


# TODO: add local cache
def load_image(filename):
    file = open(filename, 'r')

    lines = file.readlines()
    final_lines = []

    width = 0

    left_stripped = 0
    right_strip_max = 0

    for line in lines:
        stripped = line.strip()

        line_length = len(stripped)

        if line_length <= 0:
            continue
        elif line_length > width:
            width = line_length
            left_stripped = len(line) - len(line.lstrip())
            right_strip_max = len(line.rstrip())

        final_lines.append(line)

    height = len(final_lines)

    image_buffer = numpy.chararray((width, height))
    image_buffer.fill("")

    image_x = 0
    image_y = 0

    for line in final_lines:
        for char in line[left_stripped:right_strip_max]:
            image_buffer[image_x][image_y] = char

            image_x += 1

        image_x = 0
        image_y += 1

    return {"width": width, "height": height, "image_buffer": image_buffer}


def flip_image_x():
    pass
