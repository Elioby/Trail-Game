#!/usr/bin/python3

import sys
import random
import platform

from cities import cities
from survivors import survivors

# This file contains misc utility functions that have no other place

# TODO: This should return a nicely formatted date string from a datetime object ("2nd July 2009")
def format_date(datetime_object):
    return str(datetime_object.date())

# TODO: This should return a nicely formatted time string from a datetime object ("8:56 am")
def format_time(datetime_object):
    return str(datetime_object.time())

def get_next_city(distance):
	chosen_city = None

	for city in cities.values():
		distance_from_start = city["distance_from_start"]

		if distance_from_start > distance:
			if chosen_city == None or distance_from_start < chosen_city["distance_from_start"]:
				chosen_city = city

	return chosen_city


def get_random_survivor(if_player=True, if_bitten=True, if_zombified=False, if_dead=False):
	survivor_count = len(survivors)

	while True:
		random_survivor_index = random.randrange(survivor_count)

		if not if_player and random_survivor_index == 0:
			continue

		random_survivor = survivors[random_survivor_index]

		if not if_bitten and random_survivor["bitten"]:
			continue

		if not if_dead and not random_survivor["alive"]:
			continue

		if not if_zombified and random_survivor["zombified"]:
			continue

		return random_survivor

def count_survivors(if_player=True, if_bitten=True, if_zombified=False, if_dead=False):
	survivor_count = len(survivors)

	remaining_survivor_count = 0

	for survivor_index in range(survivor_count):
		if not if_player and survivor_index == 0:
			continue

		random_survivor = survivors[survivor_index]

		if not if_bitten and random_survivor["bitten"]:
			continue

		if not if_dead and not random_survivor["alive"]:
			continue

		if not if_zombified and random_survivor["zombified"]:
			continue

		remaining_survivor_count += 1

	return remaining_survivor_count

def wait_key():
    result = None
    if platform.system() == "Windows":
        import msvcrt
        result = msvcrt.getch()
    else:
        import termios
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        try:
            result = sys.stdin.read(1)
        except IOError:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    return result

