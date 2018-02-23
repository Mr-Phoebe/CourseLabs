#!/usr/bin/python
import sys

make_dict = {}
color_dict = {}

current_key = None
current_value = None
number = 0
for line in sys.stdin:
	key, value = map(str.strip, line.split('\t',1))
	key = key[1:]
	key, value = map(str.strip, key.split(',',1))
	if current_value == value:
		number += 1
	else:
		if current_value != None:
			print("{0}\t{1}, {2}".format(current_key, current_value, number))
		number = 1
		current_value = value
		current_key = key

if current_value != None:
	print("{0}\t{1}, {2}".format(current_key, current_value, number))
