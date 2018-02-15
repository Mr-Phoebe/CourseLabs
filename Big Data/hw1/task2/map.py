#!/usr/bin/env python
import sys

for line in sys.stdin:
    line = line.strip()
    cells = line.split(',')
    print("{0}\t{1}".format(cells[2],1))