import duckdb
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
DB_FILE = os.path.join(DATA_DIR, "metadata.duckdb")
PARQUET_FILE = os.path.join(DATA_DIR, "weather_data.parquet")

# Connect to the metadata DB
con = duckdb.connect(DB_FILE)

# Show tables
print("Tables:", con.execute("SHOW TABLES").fetchall())

# Query metadata
df_metadata = con.execute("SELECT * FROM weather_logs LIMIT 10").fetchdf()
print("Metadata:\n", df_metadata)

# Query Parquet data directly
df_weather = con.execute(f"SELECT * FROM read_parquet('{PARQUET_FILE}') LIMIT 10").fetchdf()
print("Weather:\n", df_weather)
