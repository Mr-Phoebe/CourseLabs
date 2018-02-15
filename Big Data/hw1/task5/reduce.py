#!/usr/bin/python
import sys

currentkey = None
count = 0
max_license = None
max_value = 0



for line in sys.stdin:
	key, value = line.split('\t',1)
	if currentkey == None:
		currentkey = key
		max_license = key
		count += 1
	elif currentkey == key:
		count += 1
	else:
		if count > max_value:
			max_license = currentkey
			max_value = count
		count = 1
		currentkey = key


if count > max_value:
	max_license = currentkey
	max_value = count

print('{0}\t{1}'.format(max_license, max_value))

