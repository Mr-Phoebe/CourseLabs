import sys
from csv import reader
from pyspark import SparkContext

saveas = "task3.out"

sc = SparkContext()
df = sc.textFile(sys.argv[1], 1)
df = df.mapPartitions(lambda x: reader(x))

def fmt(key, tot, count):
    avg = float(tot/count)
    return '%s\t%.2f,%.2f' % (key, tot, avg)

res = df.map(lambda x: (x[2], float(x[12]))) \
        .combineByKey(
            lambda v: (v, 1),
            lambda x, v: (x[0] + v, x[1] + 1),
            lambda x, y: (x[0] + y[0], x[1] + y[1])
        )

res = res.map(lambda x: fmt(x[0], x[1][0], x[1][1]))

res.saveAsTextFile(saveas)
sc.stop()

