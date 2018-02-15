#!/usr/bin/python
import sys

make_dict = {}
color_dict = {}

for line in sys.stdin:
	key, value = map(str.strip, line.split('\t',1))
	if key == 'Make':
		make_dict[value] = 1 if value not in make_dict else make_dict[value]+1
	else:
		color_dict[value] = 1 if value not in color_dict else color_dict[value]+1

make_list = sorted(make_dict.items(), key = lambda item:item[0])

for item in make_list:
	print("Make\t{0}, {1}".format(item[0], item[1]))

color_list = sorted(color_dict.items(), key = lambda item:item[0])

for item in color_list:
	print("Color\t{0}, {1}".format(item[0], item[1]))