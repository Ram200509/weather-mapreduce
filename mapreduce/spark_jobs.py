from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, avg, sum as spark_sum, max as spark_max, min as spark_min, count

spark = SparkSession.builder.appName("WeatherMapReduce").master("local[*]").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

df = spark.read.option("header", True).option("inferSchema", True).csv("../data/weather_data.csv")
df = df.withColumn("Year", year(col("Date"))).withColumn("Month", month(col("Date")))

print("\n===== JOB 1: Average Temperature by City and Year =====")
avg_temp = (
    df.groupBy("City", "Year")
    .agg(avg("Temp_Avg").alias("Avg_Temp"))
    .orderBy("City", "Year")
)
avg_temp.show(20)
avg_temp.toPandas().to_csv("../output/avg_temp_city_year.csv", index=False)

print("\n===== JOB 2: Total Rainfall by City and Month =====")
rainfall = (
    df.groupBy("City", "Month")
    .agg(spark_sum("Rainfall_mm").alias("Total_Rainfall"))
    .orderBy("City", "Month")
)
rainfall.show(20)
rainfall.toPandas().to_csv("../output/rainfall_city_month.csv", index=False)

print("\n===== JOB 3: Summer Average Temperature by City =====")
summer_temp = (
    df.filter(col("Season") == "Summer")
    .groupBy("City")
    .agg(avg("Temp_Avg").alias("Avg_Summer_Temp"))
    .orderBy(col("Avg_Summer_Temp").desc())
)
summer_temp.show()
summer_temp.toPandas().to_csv("../output/summer_temp_city.csv", index=False)

print("\n===== JOB 4: Extreme Heat Days (Temp_Max > 38) =====")
heat = (
    df.filter(col("Temp_Max") > 38)
    .groupBy("City")
    .agg(count("*").alias("Extreme_Heat_Days"))
    .orderBy(col("Extreme_Heat_Days").desc())
)
heat.show()
heat.toPandas().to_csv("../output/extreme_heat_days.csv", index=False)

print("\nJobs completed. CSV files saved in the output folder.")
spark.stop()