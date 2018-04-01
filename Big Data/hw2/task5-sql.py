import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

PV = '/user/ecc290/HW1data/parking-violations-header.csv'
OV = '/user/ecc290/HW1data/open-violations-header.csv'

spark = SparkSession.builder.appName("hw2").config("spark.some.config.option", "some-value").getOrCreate()

pv = spark.read.format('csv').options(header='true', inferschema='true').load(PV)#sys.argv[1])
pv.createOrReplaceTempView("parking")       

result = spark.sql("SELECT plate_id, registration_state, COUNT(*) AS cnt\
                    FROM parking \
                    GROUP BY plate_id, registration_state \
                    ORDER BY COUNT(*) DESC\
                    LIMIT 1")

result.select(format_string('%s, %s\t%d',result.plate_id, result.registration_state, result.cnt)).write.save("task5-sql.out",format="text")
