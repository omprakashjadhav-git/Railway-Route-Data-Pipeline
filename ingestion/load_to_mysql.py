# import mysql.connector
# from getpass import getpass

# print("Connecting to MySQL...")

# password = getpass("Enter MySQL password: ")

# connection = mysql.connector.connect(
#     host="localhost",
#     port=3306,
#     user="root",
#     password=password,
#     database="train_delay"
# )

# # print("Connected to MySQL successfully!")

# # connection.close()

# import mysql.connector
# from getpass import getpass

# password = getpass("Enter MySQL password: ")

# connection = mysql.connector.connect(
#     host="localhost",
#     port=3306,
#     user="root",
#     password=password,
#     database="train_delay"
# )

# cursor = connection.cursor()

# cursor.execute("SELECT COUNT(*) FROM train_routes_enriched")

# count = cursor.fetchone()[0]

# print("Current rows in train_routes_enriched:", count)

# cursor.close()
# connection.close()

# import mysql.connector
# from getpass import getpass
# import csv

# CSV_FILE = "data/processed/train_routes_enriched.csv"

# password = getpass("Enter MySQL password: ")

# connection = mysql.connector.connect(
#     host="localhost",
#     port=3306,
#     user="root",
#     password=password,
#     database="train_delay"
# )

# cursor = connection.cursor()

# print("Connected to MySQL.")
# print("Starting data load...")

# insert_query = """
# INSERT INTO train_routes_enriched (
#     train_number,
#     train_name,
#     station_code,
#     station_name,
#     sequence,
#     arrival_time,
#     departure_time,
#     journey_day,
#     state,
#     zone,
#     latitude,
#     longitude,
#     next_station_code,
#     next_latitude,
#     next_longitude,
#     distance_km,
#     cumulative_distance_km,
#     total_route_distance_km,
#     remaining_distance_km
# )
# VALUES (
#     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
#     %s, %s, %s, %s, %s, %s, %s, %s, %s
# )
# """

# batch = []
# batch_size = 5000
# total_loaded = 0

# with open(CSV_FILE, "r", encoding="utf-8") as file:
#     reader = csv.reader(file)

#     # Skip CSV header
#     next(reader)

#     for row in reader:

#         # Convert empty values to None for MySQL NULL
#         row = [None if value == "" else value for value in row]

#         batch.append(row)

#         if len(batch) == batch_size:
#             cursor.executemany(insert_query, batch)
#             connection.commit()

#             total_loaded += len(batch)

#             print(f"Loaded rows: {total_loaded}")

#             batch = []

#     # Load remaining rows
#     if batch:
#         cursor.executemany(insert_query, batch)
#         connection.commit()

#         total_loaded += len(batch)

# print("\nData loading completed!")
# print("Total rows loaded:", total_loaded)

# cursor.close()
# connection.close()

import mysql.connector
from getpass import getpass

password = getpass("Enter MySQL password: ")

connection = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password=password,
    database="train_delay"
)

cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM train_routes_enriched")

count = cursor.fetchone()[0]

print("Rows in MySQL:", count)

cursor.execute("""
    SELECT
        train_number,
        station_code,
        station_name,
        distance_km,
        cumulative_distance_km,
        remaining_distance_km
    FROM train_routes_enriched
    LIMIT 5
""")

print("\nSample records:")

for row in cursor.fetchall():
    print(row)

cursor.close()
connection.close()