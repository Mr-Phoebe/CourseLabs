import sys
from csv import reader
from pyspark import SparkContext

saveas = "task7.out"
t_days = ['05','06','12','13','19','20','26','27']

sc = SparkContext()
df = sc.textFile(sys.argv[1], 1)
df = df.mapPartitions(lambda x: reader(x))

res = df.map(lambda x: (x[2], (1, 0) if x[1][-2:] in t_days else (0, 1))) \
    .reduceByKey(lambda x, y: (x[0]+y[0], x[1]+y[1])) \
    .map(lambda x: '%s\t%.2f, %.2f' % (x[0], float(x[1][0]/8.0), float(x[1][1]/23.0)) )

res.saveAsTextFile(saveas)
sc.stop()