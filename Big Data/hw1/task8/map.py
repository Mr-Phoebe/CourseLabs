#!/usr/bin/python
import sys
import csv

lines = csv.reader(sys.stdin)
for line in lines:
	print("0vehicle_make,{0}\t1".format(line[20].strip()))
	print("1vehicle_color,{0}\t1".format(line[19].strip()))
