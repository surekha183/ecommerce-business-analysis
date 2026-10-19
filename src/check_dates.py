
from pathlib import Path
import pandas as pd

# Locate the original, unchanged orders file.
file_path = Path("data/raw/olist_orders_dataset.csv")

# Read timestamps as text so Pandas does not interpret them yet.
orders = pd.read_csv(file_path, dtype=str)

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

for column in date_columns:
    print("\n" + "=" * 55)
    print("COLUMN:", column)

    # Display the first ten non-empty original values.
    samples = orders[column].dropna().head(10)
    print("Original values:")
    print(samples.to_list())

    # Test parsing with day-first interpretation.
    parsed = pd.to_datetime(
        orders[column],
        dayfirst=True,
        errors="coerce"
    )

    # Count values that existed but could not be parsed.
    invalid = (
        orders[column].notna()
        & parsed.isna()
    )

    print("Non-empty original values:", int(orders[column].notna().sum()))
    print("Unparseable values:", int(invalid.sum()))
