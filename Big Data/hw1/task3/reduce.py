#!/usr/bin/env python
import sys
import csv   
    
current_key = None


for line in sys.stdin:
    key, value = line.strip().split('\t', 1)
    if current_key == None:
        current_key = key
        due_list = []
        due_list.append(value)
    elif current_key == key:
        due_list.append(value)
    else:
        total = sum(map(float, due_list))
        average = total/len(due_list)
        # print('%s\t%s,%s' % (current_key,round(total,2),round(average,2)))
        print("{0}\t{1:.2f}, {2:.2f}".format(current_key, total, average))
        current_key = key
        due_list = []
        due_list.append(value)

total = sum(map(float, due_list))
average = total/len(due_list)
print("{0}\t{1:.2f}, {2:.2f}".format(current_key, total, average))
