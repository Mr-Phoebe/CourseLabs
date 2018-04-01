import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

PV = '/user/ecc290/HW1data/parking-violations-header.csv'
OV = '/user/ecc290/HW1data/open-violations-header.csv'

spark = SparkSession.builder.appName("hw2").config("spark.some.config.option", "some-value").getOrCreate()

pv = spark.read.format('csv').options(header='true', inferschema='true').load(PV)#sys.argv[1])
pv.createOrReplaceTempView("parking")       

result = spark.sql("SELECT IF(registration_state='NY', 'NY', 'Other') AS state, COUNT(*) AS cnt\
                    FROM parking \
                    GROUP BY IF(registration_state='NY', 'NY', 'Other')")

result.select(format_string('%s\t%d',result.state,result.cnt)).write.save("task4-sql.out",format="text")
