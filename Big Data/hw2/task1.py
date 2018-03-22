import sys
from operator import add
from csv import reader
from pyspark import SparkContext

saveas = "task1-sql.out"

PV = '/user/ecc290/HW1data/parking-violations.csv'
OV = '/user/ecc290/HW1data/open-violations.csv'

sc = SparkContext()
pv = sc.textFile(sys.argv[1], 1)
pv = pv.mapPartitions(lambda x: reader(x))

ov = sc.textFile(sys.argv[2], 1)
ov = ov.mapPartitions(lambda x: reader(x))

pv = pv.map(lambda x: (x[0], x))
ov = ov.map(lambda x: (x[0], x))

res = pv.leftOuterJoin(ov)

res = res.filter(lambda x: not x[1][1]) \
         .map(lambda x: '%s\t%s, %s, %s, %s' % (x[1][0][0], x[1][0][14], x[1][0][6], x[1][0][2], x[1][0][1]) )
res.saveAsTextFile(saveas)
sc.stop()
