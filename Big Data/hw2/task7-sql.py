import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

PV = '/user/ecc290/HW1data/parking-violations-header.csv'
OV = '/user/ecc290/HW1data/open-violations-header.csv'

spark = SparkSession.builder.appName("hw2").config("spark.some.config.option", "some-value").getOrCreate()

pv = spark.read.format('csv').options(header='true', inferschema='true').load(PV)#sys.argv[1])
pv.createOrReplaceTempView("parking")

tmp = spark.sql("SELECT violation_code, dayofmonth(issue_date) AS day\
                 FROM parking")
tmp.createOrReplaceTempView("date")

#['05','06','12','13','19','20','26','27']

result = spark.sql("SELECT violation_code, \
                           SUM(IF(day = 5 OR day = 06 OR day = 12 OR day = 13 OR day = 19 OR day = 20 OR day = 26 OR day = 27, 1, 0)) AS weekend, \
                           SUM(IF(day = 5 OR day = 06 OR day = 12 OR day = 13 OR day = 19 OR day = 20 OR day = 26 OR day = 27, 0, 1)) AS weekday\
                    FROM date \
                    GROUP BY violation_code")

result.select(format_string('%s\t%.2f, %.2f',result.violation_code, result.weekend / 8.0, result.weekday / 23.0 )).write.save("task7-sql.out",format="text")

