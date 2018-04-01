
import sys
from operator import add
from csv import reader
from pyspark import SparkContext

saveas = "task5.out"

sc = SparkContext()
df = sc.textFile(sys.argv[1], 1)
df = df.mapPartitions(lambda x: reader(x))

res = df.map(lambda x: ((x[14], x[16]), 1)) \
    .reduceByKey(add) \
    .sortBy(lambda x: x[1], False) \
    .map(lambda x: '%s, %s\t%s' % (x[0][0], x[0][1], x[1]))

res = sc.parallelize(res.take(1))
res.saveAsTextFile(saveas)
sc.stop()
