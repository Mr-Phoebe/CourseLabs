from pyspark.sql import SparkSession
spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

sailors = spark.read.json("s3://ecc022618/sailors.json")
boats = spark.read.json("s3://ecc022618/boats.json")
reserves = spark.read.json("s3://ecc022618/reserves.json")

sailors.createOrReplaceTempView("sailors")
reserves.createOrReplaceTempView("reserves")
boats.createOrReplaceTempView("boats")

spark.sql("SELECT rating, AVG(age) FROM sailors \
    GROUP BY rating ORDER BY rating")\
    .coalesce(1)\
    .write.save("s3://hw022618/averageage.csv",format="csv")
