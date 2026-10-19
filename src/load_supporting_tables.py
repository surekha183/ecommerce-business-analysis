
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv
import os


# 1. Find the project folder
PROJECT_DIR = Path(__file__).resolve().parents[1]

# 2. Load database settings
load_dotenv(PROJECT_DIR / ".env")

# 3. Check required settings
required_settings = [
    "PGHOST",
    "PGPORT",
    "PGDATABASE",
    "PGUSER",
    "PGPASSWORD",
]

missing_settings = [
    setting for setting in required_settings
    if not os.getenv(setting)
]

if missing_settings:
    raise ValueError(f"Missing .env settings: {missing_settings}")

# 4. Build the database connection
connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
    host=os.getenv("PGHOST"),
    port=int(os.getenv("PGPORT")),
    database=os.getenv("PGDATABASE"),
)

engine = create_engine(connection_url)

# 5. Define the two CSV files and their PostgreSQL table names
tables = {
    "olist_order_items_dataset.csv": "olist_order_items_dataset",
    "olist_sellers_dataset.csv": "olist_sellers_dataset",
}

# 6. Load each CSV and upload it
for filename, table_name in tables.items():
    csv_path = PROJECT_DIR / "data" / "raw" / filename

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    data = pd.read_csv(csv_path)

    print(f"\nLoading: {filename}")
    print("CSV rows:", len(data))

    data.to_sql(
        name=table_name,
        con=engine,
        schema="public",
        if_exists="replace",
        index=False,
        chunksize=1000,
        method="multi",
    )

    print(f"Uploaded table: public.{table_name}")

# 7. Verify the uploaded row counts
with engine.connect() as connection:
    for table_name in tables.values():
        from sqlalchemy import text

        count = connection.execute(
            text(f"SELECT COUNT(*) FROM public.{table_name}")
        ).scalar_one()

        print(f"{table_name}: {count} rows in PostgreSQL")

engine.dispose()
print("\nSupporting tables loaded successfully.")
