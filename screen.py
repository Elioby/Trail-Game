#!/usr/bin/python3

# This file contains functions to help you operate the screen, such as clearing, drawing and flushing
# 	This is only for complex screens like the traveling screen, for other screens, use the print and input functions 

import os
import pip
import sys
import math
import time
import shutil
import platform
import subprocess

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

from debug import *

width = 0
height = 0

back_buffer = None

def init():
	global back_buffer
	global width
	global height

	width = shutil.get_terminal_size()[0] - 1
	height = shutil.get_terminal_size()[1] - 1

	back_buffer = numpy.chararray((width, height))

	back_buffer.fill("")

def clear():
	if platform.system() == "Windows":
		os.system('cls')
	else:
		os.system('clear')

def get_width():
	return width

def get_height():
	return height

def draw_rect(rect_x, rect_y, rect_width, rect_height, fill = True):
	min_x = max(rect_x, 0)
	max_x = min(rect_x + rect_width, width)

	min_y = max(rect_y, 0)
	max_y = min(rect_y + rect_height, height)

	for x in range(min_x, max_x):
		for y in range(min_y, max_y):
			back_buffer[x][y] = "#"

def set_cursor(cursor_x, cursor_y):
	sys.stdout.write("\033[" + str(cursor_x) + ";" + str(cursor_y) + "H")

def flush():
	clear()

	for col in back_buffer.T:
		content = ""
		for cell in col:
			cell_string = str(cell)[2:3]
			if cell_string != "":
				content += cell_string
			else:
				content += " "

		print(content)

	back_buffer.fill("")