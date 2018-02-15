#!/usr/bin/env python
import sys
import string
import csv

csv_reader= csv.reader(sys.stdin, delimiter=',')
for cells in csv_reader:
    print("{0}\t{1}".format(cells[2], cells[12]))