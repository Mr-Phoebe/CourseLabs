#!/usr/bin/python
import sys
import csv

lines=csv.reader(sys.stdin)
for line in lines:
	a=line[2].strip()
	weekend=['05','06','12','13','19','20','26','27']
	date=line[1]
	if date[-2:] in weekend:
		print('%s\t%d' % (a,1))
	else:
		print('%s\t%d' % (a,0))

	