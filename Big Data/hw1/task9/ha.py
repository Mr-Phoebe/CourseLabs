from __future__ import print_function
import pandas as pd
import csv

'''
parkdata = pd.read_csv('parking-violations.csv', header=None, dtype=str)
opendata = pd.read_csv('open-violations.csv', header=None, dtype=str)

parkdata = parkdata[[0, 14]].fillna(' ')
opendata = opendata[[0, 1]].fillna(' ')
parkdata.columns = ['key', 'value']
opendata.columns = ['key', 'value']

result = pd.merge(parkdata, opendata, how='inner', 
                    on='key')
print(result[result['value_x'] != result['value_y']])

'''


parkdic = {}
opendic = {}
'''
with open("parking-violations.csv", 'rb') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')

    for line in lines:
        key = line[0].strip()
        parkdic[key] = line
'''
with open("open-violations.csv", 'rb') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')

    for line in lines:
        key = line[0].strip()
        if key in opendic:
            print(key)
        opendic[key] = line
'''
for key, line in parkdic.items():
    if key in opendic:
        if line[14].strip() != opendic[key][1].strip():
            print(key, line[14].strip(), opendic[key][1].strip())
'''
'''
parklist = {}
openlist = []

with open("parking-violations.csv", 'rb') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')

    for line in lines:
        if line[0].strip() not in parklist:
            parklist[line[0].strip()] = 1
        else:
            print(line[0].strip())


with open("open-violations.csv", 'rb') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')

    for line in lines:
        if line[0].strip() not in openlist:
            openlist.append(line[0].strip())
        else:
            print(line[0].strip())
            

for key in openlist:
    if key not in parklist:
        print(key)
'''