
# from pyspark.sql import SparkSession

# # Create a Spark session
# spark = SparkSession.builder \
#     .appName("TrainDelayProject") \
#     .master("local[*]") \
#     .getOrCreate()

# print("Spark started successfully!")
# print("Spark version:", spark.version)

# # Stop Spark
# spark.stop()

# from pyspark.sql import SparkSession

# spark = SparkSession.builder \
#     .appName("TrainDelayProject") \
#     .master("local[*]") \
#     .getOrCreate()

import os

os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["hadoop.home.dir"] = r"C:\hadoop"
os.environ["PATH"] += os.pathsep + r"C:\hadoop\bin"

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("TrainDelayProject") \
    .master("local[*]") \
    .config("spark.hadoop.home.dir", "C:\\hadoop") \
    .getOrCreate()

# Read our flattened train route data
df = spark.read.csv(
    "data/processed/train_routes_flat.csv",
    header=True,
    inferSchema=True
)

print("Total records:", df.count())

print("\nSchema:")
df.printSchema()

day1_df = df.filter(df["journey_day"] == 1)

print("Day 1 records:", day1_df.count())
print("Number of columns:", len(df.columns))

selected_df = day1_df.select(
    "train_number",
    "train_name",
    "station_code",
    "station_name"
)

selected_df.show(10, truncate=False)

print("\nFirst 5 records:")
df.show(5, truncate=False)

# from pyspark.sql.functions import col
# from pyspark.sql.functions import col, radians, sin, cos, asin, sqrt, sum as spark_sum, coalesce, lit
from pyspark.sql.functions import col, radians, sin, cos, asin, sqrt, sum as spark_sum, coalesce, lit, max as spark_max
missing_station_names = df.filter(
    col("station_name").isNull() | (col("station_name") == "")
)

print("Missing station names:", missing_station_names.count())

missing_station_names.show(truncate=False)

# Read cleaned station data
stations_df = spark.read.option(
    "multiLine", "true"
).json(
    "data/processed/stations_cleaned.json"
)

print("\nStations DataFrame:")
stations_df.printSchema()

print("Total stations:", stations_df.count())

stations_df.show(5, truncate=False)

print("\nStation coordinates:")
stations_df.select(
    "code",
    "name",
    "coordinates.latitude",
    "coordinates.longitude"
).show(5, truncate=False)

print("\nJoining train routes with station data:")

joined_df = df.join(
    stations_df,
    df["station_code"] == stations_df["code"],
    "left"
).withColumn(
    "latitude",
    col("coordinates.latitude")
).withColumn(
    "longitude",
    col("coordinates.longitude")
)

joined_df.select(
    df["train_number"],
    df["train_name"],
    df["station_code"],
    stations_df["name"].alias("master_station_name"),
    stations_df["state"],
    stations_df["zone"],
    stations_df["coordinates.latitude"].alias("latitude"),
    stations_df["coordinates.longitude"].alias("longitude")
).show(10, truncate=False)

print("\nChecking unmatched station codes:")

unmatched_df = joined_df.filter(
    stations_df["code"].isNull()
)

print("Unmatched route records:", unmatched_df.count())

from pyspark.sql.window import Window
from pyspark.sql.functions import lead

route_window = Window.partitionBy(
    "train_number"
).orderBy(
    "sequence"
)

route_with_next = joined_df \
    .withColumn(
        "next_station_code",
        lead("station_code").over(route_window)
    ) \
    .withColumn(
        "next_latitude",
        lead("latitude").over(route_window)
    ) \
    .withColumn(
        "next_longitude",
        lead("longitude").over(route_window)
    )

print("\nRoute with next station coordinates:")
route_with_next.select(
    "train_number",
    "sequence",
    "station_code",
    "latitude",
    "longitude",
    "next_station_code",
    "next_latitude",
    "next_longitude"
).show(15, truncate=False)

route_with_distance = route_with_next.withColumn(
    "distance_km",
    2 * 6371 * asin(
        sqrt(
            sin(
                (radians(col("next_latitude")) - radians(col("latitude"))) / 2
            ) ** 2
            +
            cos(radians(col("latitude"))) *
            cos(radians(col("next_latitude"))) *
            sin(
                (radians(col("next_longitude")) - radians(col("longitude"))) / 2
            ) ** 2
        )
    )
)

print("\nDistance between stations:")

route_with_distance.select(
    "train_number",
    "sequence",
    "station_code",
    "next_station_code",
    "distance_km"
).show(15, truncate=False)

print("\nSpark processing completed successfully!")

print("Final enriched records:", route_with_distance.count())

print("\nFinal schema:")
route_with_distance.printSchema()

print("\nCreating final clean DataFrame:")

final_df = route_with_distance.select(
    "train_number",
    "train_name",
    "station_code",
    "station_name",
    "sequence",
    "arrival_time",
    "departure_time",
    "journey_day",
    "state",
    "zone",
    "latitude",
    "longitude",
    "next_station_code",
    "next_latitude",
    "next_longitude",
    "distance_km"
)

print("\nFinal DataFrame schema:")
final_df.printSchema()

print("\nFinal record count:", final_df.count())

print("\nFinal sample:")
final_df.show(10, truncate=False)

print("\nCalculating cumulative distance:")

route_window_cumulative = Window.partitionBy(
    "train_number"
).orderBy(
    "sequence"
).rowsBetween(
    Window.unboundedPreceding,
    -1
)

final_df = final_df.withColumn(
    "cumulative_distance_km",
    coalesce(
        spark_sum("distance_km").over(route_window_cumulative),
        lit(0.0)
    )
)

print("\nCumulative distance:")
final_df.select(
    "train_number",
    "sequence",
    "station_code",
    "station_name",
    "distance_km",
    "cumulative_distance_km"
).show(15, truncate=False)

print("\nCalculating remaining distance:")

route_total_window = Window.partitionBy(
    "train_number"
)

final_df = final_df.withColumn(
    "total_route_distance_km",
    spark_max("cumulative_distance_km").over(route_total_window)
)

final_df = final_df.withColumn(
    "remaining_distance_km",
    col("total_route_distance_km") - col("cumulative_distance_km")
)

print("\nRoute progress:")
final_df.select(
    "train_number",
    "sequence",
    "station_code",
    "station_name",
    "cumulative_distance_km",
    "total_route_distance_km",
    "remaining_distance_km"
).show(15, truncate=False)


print("\nSaving final processed data...")

final_pdf = final_df.toPandas()

final_pdf.to_csv(
    "data/processed/train_routes_enriched.csv",
    index=False
)

print("Final data saved successfully!")

spark.stop()

