import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

PV = '/user/ecc290/HW1data/parking-violations-header.csv'
OV = '/user/ecc290/HW1data/open-violations-header.csv'

spark = SparkSession.builder.appName("hw2").config("spark.some.config.option", "some-value").getOrCreate()

ov = spark.read.format('csv').options(header='true', inferschema='true').load(ys.argv[1])
ov.createOrReplaceTempView("open")        

result = spark.sql("SELECT license_type, SUM(amount_due) AS tot, AVG(amount_due) AS avg \
                    FROM open \
                    GROUP BY license_type")
result.select(format_string('%s\t%.2f,%.2f', result.license_type, result.tot, result.avg)).write.save("task3-sql.out",format="text")