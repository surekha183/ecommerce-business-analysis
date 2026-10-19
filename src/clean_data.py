
from pathlib import Path
import pandas as pd

# --------------------------------------------------
# 1. DEFINE FILE LOCATIONS
# --------------------------------------------------

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

# Create the output folder if it does not exist.
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

INPUT_FILE = RAW_DIR / "olist_orders_dataset.csv"
OUTPUT_FILE = PROCESSED_DIR / "orders_clean.csv"


# --------------------------------------------------
# 2. LOAD THE RAW ORDERS DATA
# --------------------------------------------------

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Could not find the input file: {INPUT_FILE}"
    )

orders = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("ORDERS DATA CLEANING")
print("=" * 60)

print("Original row count:", len(orders))
print("Original column count:", len(orders.columns))


# --------------------------------------------------
# 3. CHECK DUPLICATES WITHOUT DELETING RECORDS
# --------------------------------------------------

exact_duplicates = orders.duplicated().sum()

duplicate_order_ids = orders["order_id"].duplicated(
    keep=False
).sum()

print("\nExact duplicate rows:", exact_duplicates)
print("Rows with a repeated order ID:", duplicate_order_ids)

# Flag every row whose order ID appears more than once.
orders["duplicate_order_id"] = orders["order_id"].duplicated(
    keep=False
)

# We preserve all rows until any duplicates have been investigated.


# --------------------------------------------------
# 4. CONVERT TIMESTAMP COLUMNS
# --------------------------------------------------

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]


# --------------------------------------------------
# 4. CONVERT TIMESTAMP COLUMNS CORRECTLY
# --------------------------------------------------

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

# Remember which values were present before conversion.
original_date_present = orders[date_columns].notna()

# Convert each timestamp using the exact source format.
for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column],
        format="%d-%m-%Y %H:%M",
        errors="coerce"
    )

print("\nMissing timestamps after conversion:")
print(orders[date_columns].isna().sum())

# Detect non-empty values that failed conversion.
for column in date_columns:
    invalid_count = (
        original_date_present[column]
        & orders[column].isna()
    ).sum()

    print(
        f"Invalid non-empty dates in {column}: "
        f"{int(invalid_count)}"
    )


# --------------------------------------------------
# 5. INSPECT ORDER STATUS
# --------------------------------------------------

print("\nOrder status counts:")
print(orders["order_status"].value_counts(dropna=False))


# --------------------------------------------------
# 6. DEFINE ELIGIBLE DELIVERED ORDERS
# --------------------------------------------------

orders["eligible_delivery"] = (
    orders["order_status"].eq("delivered")
    & orders["order_delivered_customer_date"].notna()
    & orders["order_estimated_delivery_date"].notna()
)

eligible = orders["eligible_delivery"]

print("\nEligible delivered orders:", int(eligible.sum()))


# --------------------------------------------------
# 7. CLASSIFY LATE AND ON-TIME DELIVERIES
# --------------------------------------------------

# Use a nullable Boolean column so ineligible orders
# remain unknown instead of being incorrectly marked on time.
orders["is_late"] = pd.Series(
    pd.NA,
    index=orders.index,
    dtype="boolean"
)

orders.loc[eligible, "is_late"] = (
    orders.loc[eligible, "order_delivered_customer_date"]
    > orders.loc[eligible, "order_estimated_delivery_date"]
)

# Calculate actual minus estimated delivery time in days.
orders["delivery_delay_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_estimated_delivery_date"]
).dt.total_seconds() / 86400

# Keep this metric only for eligible deliveries.
orders.loc[~eligible, "delivery_delay_days"] = float("nan")


# --------------------------------------------------
# 8. CALCULATE ORDER JOURNEY DURATIONS
# --------------------------------------------------

# Stage 1: Purchase to payment approval.
orders["purchase_to_approval_hours"] = (
    orders["order_approved_at"]
    - orders["order_purchase_timestamp"]
).dt.total_seconds() / 3600

# Stage 2: Payment approval to carrier handoff.
orders["approval_to_carrier_hours"] = (
    orders["order_delivered_carrier_date"]
    - orders["order_approved_at"]
).dt.total_seconds() / 3600

# Stage 3: Carrier handoff to customer delivery.
orders["carrier_to_delivery_hours"] = (
    orders["order_delivered_customer_date"]
    - orders["order_delivered_carrier_date"]
).dt.total_seconds() / 3600


# --------------------------------------------------
# 9. FLAG INVALID STAGE DURATIONS
# --------------------------------------------------

duration_columns = [
    "purchase_to_approval_hours",
    "approval_to_carrier_hours",
    "carrier_to_delivery_hours",
]

for column in duration_columns:
    invalid_column = f"invalid_{column}"

    # True means the recorded stage duration is negative.
    orders[invalid_column] = orders[column] < 0

    # Replace impossible negative durations with missing values.
    # Keep the flag so we can report the data-quality issue.
    orders.loc[orders[invalid_column], column] = float("nan")

print("\nNegative stage-duration counts:")
for column in duration_columns:
    print(
        f"{column}:",
        int(orders[f"invalid_{column}"].sum())
    )


# --------------------------------------------------
# 10. CREATE A PURCHASE MONTH FIELD
# --------------------------------------------------

orders["purchase_month"] = (
    orders["order_purchase_timestamp"]
    .dt.to_period("M")
    .astype("string")
)


# --------------------------------------------------
# 11. CALCULATE SUMMARY METRICS
# --------------------------------------------------

eligible_orders = orders.loc[eligible]

late_count = int(eligible_orders["is_late"].sum())
on_time_count = int((~eligible_orders["is_late"]).sum())
eligible_count = len(eligible_orders)

print("\nDELIVERY SUMMARY")
print("-" * 40)
print("Eligible delivered orders:", eligible_count)
print("Late orders:", late_count)
print("On-time or early orders:", on_time_count)

if eligible_count > 0:
    late_rate = late_count / eligible_count * 100
    print(f"Late delivery rate: {late_rate:.2f}%")
else:
    print("Late delivery rate: unavailable (no eligible orders)")

print("\nOrders by status:")
print(orders["order_status"].value_counts(dropna=False))

print("\nRows with repeated order IDs:")
print(int(orders["duplicate_order_id"].sum()))


# --------------------------------------------------
# 12. SAVE THE CLEANED DATA
# --------------------------------------------------

orders.to_csv(OUTPUT_FILE, index=False)

print("\nSaved cleaned data to:", OUTPUT_FILE)
print("Final row count:", len(orders))
print("Final column count:", len(orders.columns))
print("\nCleaning script completed.")
