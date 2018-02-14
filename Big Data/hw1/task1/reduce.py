#!/usr/bin/env python
import sys
import csv   
    
current_key = None



for line in sys.stdin:
    line = line.strip()
    key, value = line.split('\t', 1)
    value=value.split("\t")
    if current_key == None:
        value_list=[]
        current_key=key
        value_list.append(value)
    else:
        if current_key==key:
            value_list.append(value)
        else:
            sum_list=[int(last[-1]) for last in value_list]
            sum_values=sum(sum_list)
            if sum_values==0:
                print('%s\t%s,%s,%s,%s' % (current_key, value_list[0][0],value_list[0][1],value_list[0][2],value_list[0][3]))
            current_key=key
            value_list=[]
            value_list.append(value)

sum_list=[int(last[-1]) for last in value_list]
sum_values=sum(sum_list)
if sum_values==0:
        print('%s\t%s,%s,%s,%s' % (current_key, value_list[0][0],value_list[0][1],value_list[0][2],value_list[0][3]))




