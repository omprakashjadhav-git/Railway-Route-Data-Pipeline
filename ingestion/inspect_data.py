# import json

# # with open("data/raw/trains.json", "r", encoding="utf-8") as file:
# #     trains = json.load(file)
# # print(type(trains))
# # print(trains)

# with open("data/raw/stations.json", "r", encoding="utf-8") as file:
#     stations = json.load(file)

# print(type(stations))
# print(stations[:3])


import json

# Load train data
with open("data/raw/trains.json", "r", encoding="utf-8") as file:
    trains = json.load(file)

print("Train data type:", type(trains))
print("Total trains:", len(trains))
print("First train:")
print(json.dumps(trains[0], indent=4, ensure_ascii=False))

# Load station data
with open("data/raw/stations.json", "r", encoding="utf-8") as file:
    stations = json.load(file)

print("\nStation data type:", type(stations))
print("Total stations:", len(stations))
print("First 3 stations:")
print(json.dumps(stations[:3], indent=4, ensure_ascii=False))

# Check duplicate train numbers

train_numbers = [train["trainNumber"] for train in trains]

unique_train_numbers = set(train_numbers)

print("\n--- Train Number Quality Check ---")
print("Total train records:", len(train_numbers))
print("Unique train numbers:", len(unique_train_numbers))
print("Duplicate train numbers:", len(train_numbers) - len(unique_train_numbers))

# Check duplicate station codes

station_codes = [station["code"] for station in stations]

unique_station_codes = set(station_codes)

print("\n--- Station Code Quality Check ---")
print("Total station records:", len(station_codes))
print("Unique station codes:", len(unique_station_codes))
print("Duplicate station codes:", len(station_codes) - len(unique_station_codes))

# Check missing station information

missing_state = 0
missing_zone = 0
missing_address = 0

for station in stations:
    if not station["state"]:
        missing_state += 1

    if not station["zone"]:
        missing_zone += 1

    if not station["address"]:
        missing_address += 1

print("\n--- Station Missing Value Check ---")
print("Missing state:", missing_state)
print("Missing zone:", missing_zone)
print("Missing address:", missing_address)

# Check invalid station coordinates

invalid_coordinates = 0

for station in stations:
    longitude = station["coordinates"]["longitude"]
    latitude = station["coordinates"]["latitude"]

    if longitude == 0 and latitude == 0:
        invalid_coordinates += 1

print("\n--- Station Coordinate Quality Check ---")
print("Invalid coordinates (0,0):", invalid_coordinates)

# Check train route quality

empty_routes = 0
total_route_records = 0
missing_route_station_codes = 0

for train in trains:
    route = train["completeOrderedRoute"]

    if not route:
        empty_routes += 1

    total_route_records += len(route)

    for station in route:
        if not station.get("stationCode"):
            missing_route_station_codes += 1

print("\n--- Train Route Quality Check ---")
print("Trains with empty routes:", empty_routes)
print("Total route records:", total_route_records)
print("Route records with missing station code:", missing_route_station_codes)

# Check route distance quality

zero_distance_records = 0
total_route_records = 0

for train in trains:
    for station in train["completeOrderedRoute"]:
        total_route_records += 1

        if station.get("distance") == 0:
            zero_distance_records += 1

print("\n--- Route Distance Quality Check ---")
print("Total route records:", total_route_records)
print("Route records with distance 0:", zero_distance_records)