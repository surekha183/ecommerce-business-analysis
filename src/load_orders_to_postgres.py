
from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


# 1. Find the project folder
PROJECT_DIR = Path(__file__).resolve().parents[1]

# 2. Load database settings from the .env file
load_dotenv(PROJECT_DIR / ".env")

# 3. Locate the cleaned CSV file
CSV_FILE = PROJECT_DIR / "data" / "processed" / "orders_clean.csv"

# 4. Check that the CSV file exists
if not CSV_FILE.exists():
    raise FileNotFoundError(f"CSV file not found: {CSV_FILE}")

# 5. Read the database connection settings
required_settings = [
    "PGHOST",
    "PGPORT",
    "PGDATABASE",
    "PGUSER",
    "PGPASSWORD",
]

missing_settings = [
    setting
    for setting in required_settings
    if not os.getenv(setting)
]

if missing_settings:
    raise ValueError(
        f"Missing settings in .env: {missing_settings}"
    )

# 6. Build the PostgreSQL connection URL safely
connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
    host=os.getenv("PGHOST"),
    port=int(os.getenv("PGPORT")),
    database=os.getenv("PGDATABASE"),
)

# 7. Create the database engine
engine = create_engine(connection_url)

# 8. Test the database connection
with engine.connect() as connection:
    database_name = connection.execute(
        text("SELECT current_database();")
    ).scalar_one()

print("Connected to database:", database_name)

# 9. Load the cleaned CSV into pandas
orders = pd.read_csv(CSV_FILE)

print("CSV rows:", len(orders))
print("CSV columns:", len(orders.columns))

# 10. Convert timestamp columns into datetime values
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
        errors="coerce",
    )

# 11. Convert Boolean columns consistently
boolean_columns = [
    "eligible_delivery",
    "is_late",
    "invalid_purchase_to_approval_hours",
    "invalid_approval_to_carrier_hours",
    "invalid_carrier_to_delivery_hours",
]

def parse_boolean(value):
    if pd.isna(value):
        return pd.NA

    if isinstance(value, bool):
        return value

    value = str(value).strip().lower()

    if value == "true":
        return True

    if value == "false":
        return False

    raise ValueError(f"Unexpected Boolean value: {value}")

for column in boolean_columns:
    orders[column] = (
        orders[column]
        .map(parse_boolean)
        .astype("boolean")
    )

# 12. Upload the data into a PostgreSQL table
orders.to_sql(
    name="orders",
    con=engine,
    schema="public",
    if_exists="replace",
    index=False,
    chunksize=1000,
    method="multi",
)

print("CSV uploaded to PostgreSQL table: public.orders")

# 13. Verify the uploaded row count
with engine.connect() as connection:
    database_rows = connection.execute(
        text("SELECT COUNT(*) FROM public.orders;")
    ).scalar_one()

print("Rows in PostgreSQL:", database_rows)

# 14. Confirm that the upload preserved every row
if database_rows != len(orders):
    raise ValueError(
        f"Row count mismatch: CSV={len(orders)}, "
        f"PostgreSQL={database_rows}"
    )

print("SUCCESS: CSV and PostgreSQL row counts match.")

# 15. Close the database engine
engine.dispose()
