#!/usr/bin/python
import sys
import csv
import sys

lines = csv.reader(sys.stdin)
for line in lines:
	a = line[14].strip()
	b = line[16].strip()
	print("{0}, {1}\t1".format(a, b))
