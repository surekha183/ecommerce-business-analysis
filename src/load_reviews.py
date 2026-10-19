
from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# Find the project folder
PROJECT_DIR = Path(__file__).resolve().parents[1]

# Load database credentials
load_dotenv(PROJECT_DIR / ".env")

# Locate the reviews CSV
csv_path = (
    PROJECT_DIR
    / "data"
    / "raw"
    / "olist_order_reviews_dataset.csv"
)

if not csv_path.exists():
    raise FileNotFoundError(f"CSV not found: {csv_path}")

# Build the database connection
connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
    host=os.getenv("PGHOST"),
    port=int(os.getenv("PGPORT")),
    database=os.getenv("PGDATABASE"),
)

engine = create_engine(connection_url)

# Read the review data
reviews = pd.read_csv(csv_path)

print("Review CSV rows:", len(reviews))

# Upload the reviews table
reviews.to_sql(
    name="olist_order_reviews_dataset",
    con=engine,
    schema="public",
    if_exists="replace",
    index=False,
    chunksize=1000,
    method="multi",
)

# Verify the upload
from sqlalchemy import text

with engine.connect() as connection:
    count = connection.execute(
        text("SELECT COUNT(*) FROM public.olist_order_reviews_dataset;")
    ).scalar_one()

print("Review rows in PostgreSQL:", count)
print("Reviews table loaded successfully.")

engine.dispose()
