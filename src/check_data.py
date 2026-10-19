
from pathlib import Path
import pandas as pd

# Folder containing the original CSV files
DATA_DIR = Path("data/raw")

# Inspect every CSV file without modifying it
for file_path in sorted(DATA_DIR.glob("*.csv")):
    print("\n" + "=" * 60)
    print("FILE:", file_path.name)

    # Read the CSV
    df = pd.read_csv(file_path)

    # Display basic information
    print("Number of rows:", len(df))
    print("Number of columns:", len(df.columns))
    print("Column names:", df.columns.tolist())

    # Show missing values only when present
    missing = df.isna().sum()
    missing = missing[missing > 0]

    if not missing.empty:
        print("Missing values:")
        print(missing.to_dict())
    else:
        print("Missing values: None")
