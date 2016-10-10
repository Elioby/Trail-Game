#!/usr/bin/python3

from survivors import survivors

# This file contains misc utility functions that have no other place

# TODO: This should return a nicely formatted date string from a datetime object ("2nd July 2009")
def format_date(datetime_object):
    return str(datetime_object.date())

# TODO: This should return a nicely formatted time string from a datetime object ("8:56 am")
def format_time(datetime_object):
    return str(datetime_object.time())

# TODO: This should return a single random survivor from the list in survivors.py
# TODO: If if_player is false, don't return the player, if if_infected is false, don't return any infected players, 
# TODO: If if_dead is false, don't return any dead players
def get_random_survivor(if_player=True, if_infected=True, if_dead=False):
	return survivors[0]