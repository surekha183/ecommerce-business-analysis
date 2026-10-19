
from pathlib import Path
import pandas as pd

# Read the cleaned orders table.
file_path = Path("data/processed/orders_clean.csv")
orders = pd.read_csv(file_path)

# Convert the original timestamp columns back to datetime values.
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce"
    )

# Find orders with a carrier handoff before approval.
invalid_handoff = orders[
    orders["invalid_approval_to_carrier_hours"] == True
]

print("Invalid approval-to-carrier rows:", len(invalid_handoff))

print(
    invalid_handoff[
        [
            "order_id",
            "order_status",
            "order_approved_at",
            "order_delivered_carrier_date",
            "approval_to_carrier_hours",
        ]
    ].head(10).to_string(index=False)
)

# Find orders with delivery before carrier handoff.
invalid_transit = orders[
    orders["invalid_carrier_to_delivery_hours"] == True
]

print("\nInvalid carrier-to-delivery rows:", len(invalid_transit))

print(
    invalid_transit[
        [
            "order_id",
            "order_status",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "carrier_to_delivery_hours",
        ]
    ].head(10).to_string(index=False)
)
