#!/usr/bin/python
import sys

state_dict = {'NY' : 0, 'Other' : 0}
for line in sys.stdin:
	key, value = line.strip().split('\t',1)
	state_dict[key] += 1

for state, count in state_dict.items():
	print('%s\t%d' %(state,count))





