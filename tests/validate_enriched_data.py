
import pandas as pd

file_path = "data/processed/train_routes_enriched.csv"
df = pd.read_csv(file_path)

print("=== Final Data Quality Report ===")

print("Total records:", len(df))
print("Unique trains:", df["train_number"].nunique())

print("\nMissing values:")
print(df[["latitude", "longitude", "distance_km"]].isnull().sum())

print("\nNegative distances:", (df["distance_km"] < 0).sum())

assert len(df) == 416637, "Unexpected record count"
assert df["train_number"].nunique() == 5208, "Unexpected train count"
assert (df["distance_km"].dropna() >= 0).all(), "Negative distance found"

print("\nCore data quality checks passed!")