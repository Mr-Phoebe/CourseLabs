#!/usr/bin/env python
import sys
import string
import os
import csv

filepath = os.environ.get("mapreduce_map_input_file")
filename = os.path.split(filepath)[-1]

csv_reader= csv.reader(sys.stdin, delimiter=',')
for cells in csv_reader:
    if 'park' in filename:
        print('{0}\t{1}\t{2}\t{3}\t{4}\t{5}'.format(cells[0], cells[14], cells[6], cells[2], cells[1],0))
    else:
        print('{0}\t1'.format(cells[0]))
