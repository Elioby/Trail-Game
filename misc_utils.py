#!/usr/bin/python3

# This file contains misc utility functions that have no other place

# TODO: This should return a nicely formatted date string from a datetime object ("2nd July 2009")
def format_date(datetime_object):
    return str(datetime_object.date())

# TODO: This should return a nicely formatted time string from a datetime object ("8:56 am")
def format_time(datetime_object):
    return str(datetime_object.time())