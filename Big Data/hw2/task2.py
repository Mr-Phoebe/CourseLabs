import sys
from csv import reader
from pyspark import SparkContext

saveas = "task2.out"

sc = SparkContext()
pv = sys.argv[1]
pv = sc.textFile(pv, 1)
pv = pv.mapPartitions(lambda x: reader(x))

res = pv.map(lambda x: (x[2], 1)) \
        .reduceByKey(lambda x, y: x + y ) \
        .map(lambda x: '%s\t%s' % (x[0], x[1]) )
res.saveAsTextFile(saveas)
sc.stop()