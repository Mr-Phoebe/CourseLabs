import sys
from csv import reader
from pyspark import SparkContext

saveas = "task2.out"

sc = SparkContext()
df = sc.textFile(sys.argv[1], 1)
df = df.mapPartitions(lambda x: reader(x))

res = df.map(lambda x: (x[2], 1)) \
        .reduceByKey(lambda x, y: x + y ) \
        .map(lambda x: '%s\t%s' % (x[0], x[1]) )
res.saveAsTextFile(saveas)
sc.stop()