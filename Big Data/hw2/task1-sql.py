import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

PV = '/user/ecc290/HW1data/parking-violations-header.csv'
OV = '/user/ecc290/HW1data/open-violations-header.csv'

spark = SparkSession.builder.appName("hw2").config("spark.some.config.option", "some-value").getOrCreate()

pv = spark.read.format('csv').options(header='true', inferschema='true').load(sys.argv[1])
pv.createOrReplaceTempView("parking")

ov = spark.read.format('csv').options(header='true', inferschema='true').load(sys.argv[2])
ov.createOrReplaceTempView("open")        

result = spark.sql("SELECT p.summons_number, p.plate_id, p.violation_precinct, p.violation_code, date_format(p.issue_date, 'yyyy-MM-dd') as issue_date \
           FROM parking p LEFT JOIN open o ON p.summons_number = o.summons_number \
           WHERE o.fine_amount IS NULL ")
result.select(format_string('%d\t%s, %d, %d, %s',result.summons_number,result.plate_id,result.violation_precinct,result.violation_code, result.issue_date)).write.save("task1-sql.out",format="text")