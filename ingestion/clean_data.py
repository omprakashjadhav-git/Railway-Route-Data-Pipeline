import json

# Load raw train data
with open("data/raw/trains.json", "r", encoding="utf-8") as file:
    trains = json.load(file)

# Load raw station data
with open("data/raw/stations.json", "r", encoding="utf-8") as file:
    stations = json.load(file)

print("Raw trains:", len(trains))
print("Raw stations:", len(stations))


# Clean invalid station coordinates

cleaned_stations = []

for station in stations:
    longitude = station["coordinates"]["longitude"]
    latitude = station["coordinates"]["latitude"]

    if longitude == 0 and latitude == 0:
        station["coordinates"]["longitude"] = None
        station["coordinates"]["latitude"] = None

    cleaned_stations.append(station)

print("Cleaned stations:", len(cleaned_stations))

from pathlib import Path

# Create processed data directory
processed_dir = Path("data/processed")
processed_dir.mkdir(parents=True, exist_ok=True)

# Save cleaned station data
with open(processed_dir / "stations_cleaned.json", "w", encoding="utf-8") as file:
    json.dump(cleaned_stations, file, indent=4, ensure_ascii=False)

print("Cleaned station data saved successfully.")

# Check train distance quality

missing_distance = 0
zero_distance = 0
negative_distance = 0

for train in trains:
    distance = train.get("overallDistanceKm")

    if distance is None:
        missing_distance += 1
    elif distance == 0:
        zero_distance += 1
    elif distance < 0:
        negative_distance += 1

print("\n--- Train Distance Quality Check ---")
print("Missing distance:", missing_distance)
print("Zero distance:", zero_distance)
print("Negative distance:", negative_distance)

# Find trains with zero overall distance

zero_distance_trains = []

for train in trains:
    if train.get("overallDistanceKm") == 0:
        zero_distance_trains.append({
            "trainNumber": train.get("trainNumber"),
            "trainName": train.get("trainName"),
            "source": train.get("source", {}).get("name"),
            "destination": train.get("destination", {}).get("name"),
            "distance": train.get("overallDistanceKm")
        })

print("\n--- Trains With Zero Distance ---")
print("Count:", len(zero_distance_trains))

for train in zero_distance_trains[:10]:
    print(train)

# Clean train data

cleaned_trains = []

for train in trains:
    distance = train.get("overallDistanceKm")

    # Remove only clearly invalid negative distances
    if distance is not None and distance < 0:
        continue

    cleaned_trains.append(train)

print("\n--- Train Cleaning ---")
print("Raw trains:", len(trains))
print("Cleaned trains:", len(cleaned_trains))
print("Removed trains:", len(trains) - len(cleaned_trains))

# Save cleaned train data

with open(processed_dir / "trains_cleaned.json", "w", encoding="utf-8") as file:
    json.dump(cleaned_trains, file, indent=4, ensure_ascii=False)

print("Cleaned train data saved successfully.")