# Weather Data Pipeline with Airflow

This project implements a weather data pipeline using Apache Airflow, a platform for programmatically authoring, scheduling, and monitoring workflows. Airflow enables DAG-based pipeline orchestration with powerful scheduling, retry, and logging mechanisms.

**Airflow Main Components Used in This Project**

- **DAG (Directed Acyclic Graph)**: The pipeline logic is defined in weather_pipeline.py, scheduled and executed by Airflow.
**Python Operators**: Used to define tasks such as fetching weather data from the OpenWeather API, parsing and saving it, and logging metadata.
- **Dockerized Deployment**: Runs fully inside Docker using docker-compose, providing isolated and reproducible local development.
- **Airflow UI**: Access the web interface at http://localhost:8080 (http://localhost:9090 in this case) to trigger DAG runs, inspect logs, and monitor pipeline performance.

### Project Structure

```
airflow_pipeline_football/
├── config/                  # Config files like API endpoints, secrets (if any)
├── dags/                    # Airflow DAGs live here
├── data/football_data       # Output directory for raw data as Parquet
├── db/                      # DuckDB file will live here
├── logs/                    # Airflow logs
├── plugins/
├── .env
├── docker-compose.yaml      # Docker services: Airflow, scheduler, webserver
├── Dockerfile
├── README.md
└── requirements.txt
```

### Running Airflow Locally

1. Start Airflow with Docker Compose

    ```bash
    docker-compose up -d
    ```

2. Access the Airflow Web UI

    URL: http://localhost:9090

    Default credentials:

        - Username: airflow
        - Password: airflow

3. Trigger the Weather DAG

    - In the Airflow UI, look for simple_weather_pipeline
    - Click “Trigger DAG” to manually run the pipeline.

### Querying Data Locally

**Using Python**

You can use `duckdb` in Python to load both the metadata and Parquet file:

    ```bash
    import duckdb

    # Query metadata
    con = duckdb.connect("data/metadata.duckdb")
    con.execute("SELECT * FROM weather_logs").df()

    # Query Parquet directly
    con.execute("SELECT * FROM read_parquet('data/weather_data.parquet')").df()
    ```

**From CLI (macOS/Linux)**

1. Install DuckDB:

    ```bash
    brew install duckdb
    ```

2. Use the shell:

    ```bash
    duckdb data/metadata.duckdb
    ```

3. Inside the DuckDB shell:

    ```bash
    SELECT * FROM weather_logs;
    SELECT * FROM read_parquet('data/weather_data.parquet');
    ```

### Scheduling and Automation

Airflow handles scheduling based on CRON expressions directly inside your DAG definition. You can edit the `schedule` in your DAG file to run every 10 minutes, for example:

`schedule`='*/10 * * * *'

Once the DAG is triggered (manually or by schedule), the tasks will:

    1. Fetch weather data from OpenWeather.
    2. Parse and convert it to a standardized format.
    3. Save it to a Parquet file.
    4. Log metadata to DuckDB.