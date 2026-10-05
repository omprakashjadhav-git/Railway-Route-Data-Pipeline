import json

# Load cleaned train data
with open("data/processed/trains_cleaned.json", "r", encoding="utf-8") as file:
    trains = json.load(file)

print("Total trains:", len(trains))

# Check the route of the first train

first_train = trains[0]

route = first_train["completeOrderedRoute"]

print("Train number:", first_train["trainNumber"])
print("Number of route stations:", len(route))
print("First route station:", route[0])

# Extract information from the first route station

first_route = route[0]

train_number = first_train["trainNumber"]
train_name = first_train["trainName"]

station_code = first_route["stationCode"]
station_name = first_route["stationName"]
sequence = first_route["sequence"]

print("\n--- First Route Record ---")
print("Train number:", train_number)
print("Train name:", train_name)
print("Station code:", station_code)
print("Station name:", station_name)
print("Sequence:", sequence)

# Create one flat route record

flat_record = {
    "train_number": train_number,
    "train_name": train_name,
    "station_code": station_code,
    "station_name": station_name,
    "sequence": sequence
}

print("\n--- Flat Record ---")
print(flat_record)

# Flatten all train routes

flat_routes = []

for train in trains:

    train_number = train["trainNumber"]
    train_name = train["trainName"]

    route = train["completeOrderedRoute"]

    for station in route:

        flat_record = {
            "train_number": train_number,
            "train_name": train_name,
            "station_code": station["stationCode"],
            "station_name": station["stationName"],
            "sequence": station["sequence"],
            "arrival_time": station["arrivalTime"],
            "departure_time": station["departureTime"],
            "journey_day": station["journeyDay"],
            "distance": station["distance"]
        }

        flat_routes.append(flat_record)

print("\n--- Flattening Result ---")
print("Total flat route records:", len(flat_routes))
print("First flat record:", flat_routes[0])
print("Last flat record:", flat_routes[-1])

import csv
from pathlib import Path

# Create processed directory if it doesn't exist
processed_dir = Path("data/processed")
processed_dir.mkdir(parents=True, exist_ok=True)

# Save flattened routes as CSV
output_file = processed_dir / "train_routes_flat.csv"

with open(output_file, "w", newline="", encoding="utf-8") as file:

    fieldnames = [
        "train_number",
        "train_name",
        "station_code",
        "station_name",
        "sequence",
        "arrival_time",
        "departure_time",
        "journey_day",
        "distance"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(flat_routes)

print("\nFlattened route data saved successfully.")
print("Output file:", output_file)

# Validate the saved CSV

with open(output_file, "r", encoding="utf-8") as file:
    row_count = sum(1 for row in file) - 1  # subtract header

print("\n--- CSV Validation ---")
print("CSV data rows:", row_count)

# Check CSV columns

with open(output_file, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    columns = next(reader)

print("\n--- CSV Columns ---")
print(columns)

# Check missing values

missing_counts = {
    "train_number": 0,
    "station_code": 0,
    "station_name": 0,
    "sequence": 0
}

with open(output_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        for column in missing_counts:
            if not row[column]:
                missing_counts[column] += 1

print("\n--- Missing Value Check ---")

for column, count in missing_counts.items():
    print(f"{column}: {count}")

# Find rows with missing station names

print("\n--- Rows with Missing Station Name ---")

with open(output_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        if not row["station_name"]:
            print(row)

# Check station code P in the cleaned station data

with open("data/processed/stations_cleaned.json", "r", encoding="utf-8") as file:
    stations = json.load(file)

print("\n--- Station Lookup ---")

for station in stations:
    if station["code"] == "P":
        print(station)

# Check duplicate route records

seen_routes = set()
duplicate_count = 0

with open(output_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:

        route_key = (
            row["train_number"],
            row["sequence"],
            row["station_code"]
        )

        if route_key in seen_routes:
            duplicate_count += 1
        else:
            seen_routes.add(route_key)

print("\n--- Duplicate Route Check ---")
print("Duplicate route records:", duplicate_count)