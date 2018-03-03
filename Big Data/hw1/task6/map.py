#!/usr/bin/python
import sys
import csv
import sys

lines=csv.reader(sys.stdin)
for line in lines:
	a=line[14].strip()
	b=line[16].strip()
	print('%s,%s\t%s' % (a,b,1))