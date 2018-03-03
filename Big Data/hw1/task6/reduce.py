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
# tuple_list = [(x,y) for x,y in whole_dict.items()]
# tuple_list = sorted(tuple_list, key = lambda tup:tup[1], reverse=True)
class Reversinator(object):
    def __init__(self, obj):
        self.obj = obj
    def __lt__(self, other):
        return other.obj < self.obj

tuple_list = sorted(whole_dict.items(), key = lambda tup:(tup[1], Reversinator(tup[0])), reverse=True)
length = len(tuple_list)

for i in range(20):
	print('{0}\t{1}'.format(tuple_list[i][0],tuple_list[i][1]))
