#!/usr/bin/env python
import sys
import string
import os
import csv


filepath=os.environ.get("mapreduce_map_input_file")
#filepath = os.environ["map_input_file"]
filename = os.path.split(filepath)[-1]
csv_reader= csv.reader(sys.stdin, delimiter=',')
for cells in csv_reader:
    #line = line.strip()
    #cells = line.split(',')
    if 'park' in filename:
        s=cells[0]
        values=[cells[14],cells[6],cells[2],cells[1],0]
        print ('%s\t%s\t%s\t%s\t%s\t%s' % (s, cells[14],cells[6],cells[2],cells[1],0))
    else:
        s=cells[0]
        values=[cells[1],cells[5],cells[9],1]
        print ('%s\t%s\t%s\t%s\t%s' % (s, cells[1],cells[5],cells[9],1))
        
    
    
                
                
     