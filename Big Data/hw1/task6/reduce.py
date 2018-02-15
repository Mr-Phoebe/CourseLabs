#!/usr/bin/python
import sys
import heapq

whole_dict = {}
current_key = None

for line in sys.stdin:
	key, value=line.split('\t',1)
	if current_key == key:
		whole_dict[current_key] += 1
	else:
		whole_dict[key] = 1
		current_key = key

'''
klist = heapq.nlargest(20,whole_dict,key=whole_dict.__getitem__)

for key in klist:
	print('%s\t%d' % (key,whole_dict[key]))
'''
tuple_list = sorted(whole_dict.items(), key = lambda tup:tup[1], reverse=True)

length = len(tuple_list)

for i in range(10):
	print('{0}\t{1}'.format(tuple_list[i][0],tuple_list[i][1]))

for i in range(length-10, length):
	print('{0}\t{1}'.format(tuple_list[i][0],tuple_list[i][1]))	