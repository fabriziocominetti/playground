from airflow.decorators import dag, task
from datetime import datetime
import requests
import pandas as pd
import duckdb
import os

DATA_DIR = "/opt/airflow/data/weather_data"
PARQUET_PATH = f"{DATA_DIR}/weather.parquet"
DUCKDB_PATH = "/opt/airflow/db/weather_metadata.duckdb"

@dag(
    start_date=datetime(2023, 1, 1),
    schedule="@daily",  # or None for manual
    catchup=False,
    tags=["weather"],
)
def simple_weather_pipeline():

    @task()
    def fetch_and_log(city: str = "Milan"):
        os.makedirs(DATA_DIR, exist_ok=True)

        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        current = data["current_condition"][0]
        record = {
            "city": city,
            "temperature_C": float(current["temp_C"]),
            "humidity": int(current["humidity"]),
            "observation_time": current["observation_time"],
            "fetched_at": datetime.utcnow().isoformat()
        }

        # Save to Parquet
        df = pd.DataFrame([record])
        if os.path.exists(PARQUET_PATH):
            old_df = pd.read_parquet(PARQUET_PATH)
            df = pd.concat([old_df, df], ignore_index=True)
        df.to_parquet(PARQUET_PATH, index=False)

        # Log to DuckDB
        conn = duckdb.connect(DUCKDB_PATH)
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

    fetch_and_log()

simple_weather_pipeline()
