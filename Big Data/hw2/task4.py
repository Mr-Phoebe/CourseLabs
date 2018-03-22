import sys
from csv import reader
from pyspark import SparkContext

saveas = "task4.out"

sc = SparkContext()
df = sc.textFile(PV, 1)
df = df.mapPartitions(lambda x: reader(x))

res = df.map(lambda x: x[16] if x[16]=='NY' else 'Other').countByValue()
res = sc.parallelize(res.items()).map(lambda x: '%s\t%s' % (x[0],x[1]) )

res.saveAsTextFile(saveas)
sc.stop()