#!/usr/bin/python
import sys
import csv

csv_reader = csv.reader(sys.stdin)
for s in csv_reader:
    if s[16] == 'NY':
        print("NY\t1")
    else:
        print("Other\t1")
               
    
