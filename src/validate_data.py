
from pathlib import Path
import pandas as pd

# Locate the cleaned orders file
file_path = Path("data/processed/orders_clean.csv")

# Stop if the cleaned file does not exist
if not file_path.exists():
    raise FileNotFoundError(f"File not found: {file_path}")

# Load the cleaned data
orders = pd.read_csv(file_path)

# Check the dataset size
print("Rows:", len(orders))
print("Columns:", len(orders.columns))

# Check whether order IDs are unique
print("Duplicate order IDs:", orders["order_id"].duplicated().sum())

# Check the delivery eligibility labels
eligible = orders["eligible_delivery"].astype(bool)
print("Eligible orders:", eligible.sum())

# Check late-delivery labels
late_count = orders.loc[eligible, "is_late"].astype(bool).sum()
on_time_count = (~orders.loc[eligible, "is_late"].astype(bool)).sum()

print("Late orders:", late_count)
print("On-time or early orders:", on_time_count)
print("Labels match eligible orders:", late_count + on_time_count == eligible.sum())

# Check invalid stage-duration flags
print(
    "Invalid approval-to-carrier durations:",
    orders["invalid_approval_to_carrier_hours"].astype(bool).sum()
)
print(
    "Invalid carrier-to-delivery durations:",
    orders["invalid_carrier_to_delivery_hours"].astype(bool).sum()
)

print("\nValidation script completed.")
