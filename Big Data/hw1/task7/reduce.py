#!/usr/bin/python
import sys
current_key=None

w_d=0
w_e=0
for line in sys.stdin:
	key, value=line.split('\t',1)
	if current_key==key:
		if int(value)==0:
			w_d+=1
		else:
			w_e+=1
	else:
		if current_key:
			print('%s\t%.2f, %.2f' % (current_key,w_e/float(8),w_d/float(23)))
		current_key=key
		w_d=0
		w_e=0
		if int(value)==0:
			w_d+=1
		else:
			w_e+=1
print('%s\t%.2f, %.2f' % (current_key,w_e/float(8),w_d/float(23)))



