#!/usr/bin/python3

# This file contains some useful debug tools

import time

debug_mode = False


def dprint(message):
    if debug_mode:
        print("DEBUG: " + str(message))
        time.sleep(0.5)
