#!/usr/bin/python
import sys
import csv

lines = csv.reader(sys.stdin)
for line in lines:
	value = line[20].strip()
	print("0vehicle_make,{0}\t1".format(value if value != "" else "NONE"))
	value = line[19].strip()
	print("1vehicle_color,{0}\t1".format(value if value != "" else "NONE"))
