from prefect import flow, task
import requests
import pandas as pd
import duckdb
from datetime import datetime
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
PARQUET_FILE = os.path.join(DATA_DIR, "weather_data.parquet")
DB_FILE = os.path.join(DATA_DIR, "metadata.duckdb")

# Step 1: Fetch data from wttr.in
@task
def fetch_weather(city: str) -> dict:
    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Step 2: Parse the response
@task
def parse_weather(data: dict, city: str) -> dict:
    current = data["current_condition"][0]
    return {
        "city": city,
        "temperature_C": float(current["temp_C"]),
        "humidity": int(current["humidity"]),
        "observation_time": current["observation_time"],
        "fetched_at": datetime.utcnow().isoformat()
    }

# Step 3: Save to Parquet
@task
def save_to_parquet(record: dict, filename: str = PARQUET_FILE):
    df = pd.DataFrame([record])
    if os.path.exists(filename):
        old_df = pd.read_parquet(filename)
        df = pd.concat([old_df, df], ignore_index=True)
    df.to_parquet(filename, index=False)

# Step 4: Log metadata to DuckDB
@task
def log_metadata(record: dict, db_file: str = DB_FILE):
    conn = duckdb.connect(database=db_file)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS weather_logs (
            city TEXT,
            temperature_C DOUBLE,
            humidity INTEGER,
            observation_time TEXT,
            fetched_at TEXT
        )
    """)
    conn.execute("""
        INSERT INTO weather_logs VALUES (?, ?, ?, ?, ?)
    """, (
        record["city"],
        record["temperature_C"],
        record["humidity"],
        record["observation_time"],
        record["fetched_at"]
    ))
    conn.close()

# Step 5: Flow
@flow
def weather_pipeline(city: str = "London"):
    raw = fetch_weather(city)
    parsed = parse_weather(raw, city)
    save_to_parquet(parsed)
    log_metadata(parsed)

# Run
if __name__ == "__main__":
    weather_pipeline("Milan")  # Change city as needed
