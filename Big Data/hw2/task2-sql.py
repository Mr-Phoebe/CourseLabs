import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

PV = '/user/ecc290/HW1data/parking-violations-header.csv'
OV = '/user/ecc290/HW1data/open-violations-header.csv'

spark = SparkSession.builder.appName("hw2").config("spark.some.config.option", "some-value").getOrCreate()

pv = spark.read.format('csv').options(header='true', inferschema='true').load(sys.argv[1])
pv.createOrReplaceTempView("parking")

res = spark.sql("SELECT violation_code, COUNT(*) AS cnt \
                FROM parking p \
                GROUP BY violation_code")

res.select(format_string('%d\t%d',res.violation_code,res.cnt)).write.save("task2-sql.out",format="text")