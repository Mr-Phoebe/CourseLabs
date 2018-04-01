import sys
from operator import add
from csv import reader
from pyspark import SparkContext

saveas = "task6.out"

class Reversinator(object):
    def __init__(self, obj):
        self.obj = obj
    def __lt__(self, other):
        return other.obj < self.obj

sc = SparkContext()
df = sc.textFile(sys.argv[1], 1)
df = df.mapPartitions(lambda x: reader(x))

res = df.map(lambda x: ((x[14], x[16]), 1)) \
    .reduceByKey(add) \
    .sortBy(lambda x: (x[1], Reversinator(x[0])), False) \
    .map(lambda x: '%s, %s\t%s' % (x[0][0], x[0][1], x[1]))

res = sc.parallelize(res.take(20))
res.saveAsTextFile(saveas)
sc.stop()


