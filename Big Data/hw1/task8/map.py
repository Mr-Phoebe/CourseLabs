#!/usr/bin/python
import sys
import csv

lines = csv.reader(sys.stdin)
for line in lines:
	print("0Make, {0}\t1".format(line[20].strip()))
	print("1Color, {0}\t1".format(line[21].strip()))