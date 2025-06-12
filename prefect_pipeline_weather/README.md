# Weather Data Pipeline with Prefect

This project implements a weather data pipeline using **Prefect**, a modern open-source workflow orchestration tool that simplifies building, scheduling, and monitoring data pipelines. Prefect handles task dependencies, retries, and logging, providing a robust and scalable framework for pipeline automation.

**Prefect Main Components Used in This Project**

- **Flows:** The main pipeline logic is defined in `main.py` as a Prefect Flow, orchestrating weather data fetching, processing, and saving.
- **Tasks:** Individual units of work within the flow, such as fetching weather data, parsing it, saving to Parquet, and logging metadata.
- **Prefect Server:** Runs locally to manage flow scheduling, state, and provides a web UI to monitor flow and task runs.
- **Prefect UI:** Accessible at `http://127.0.0.1:4200` when the server is running; used here to track flow executions and debug.

### Project Structure

```
weather_pipeline_prefect/
├── src/
    ├── main.py              # Pipeline execution script
    ├── start_worker.py      # Script to load .env and start Prefect worker
    └── query_results.py     # Python script to query metadata and parquet data
├── data/
    ├── metadata.duckdb      # Metadata logs database
    └── weather_data.parquet # Output weather data file
├── prefect.yaml             # Prefect project configuration file
├── requirements.txt
└── README.md
```

### Running Prefect UI Locally with `main.py`

1. Start a local Prefect orchestration server with:

   ```bash
   prefect server start
   ```

    - Hosts the Prefect UI at: http://127.0.0.1:4200
    - Uses a temporary SQLite backend (data lost on server stop)

2. In a separate terminal, run your pipeline:

    ```bash
    python main.py
    ```
3. Access the UI to monitor flow and task runs in real time.

### Querying Data

**From Python**

Use `query_results.py` to connect to metadata.duckdb and query both the metadata and Parquet data programmatically.

**From CLI (macOS/Linux)**

1. Install DuckDB CLI:

    ```bash
    brew install duckdb
    ```

2. Open DuckDB shell:

    ```bash
    duckdb metadata.duckdb
    ```

    - Inside DuckDB CLI: to query `.duckdb` databases, execute standard SQL queries; to query `.parquet` files directly, use the `FROM read_parquet('table_name.parquet')` syntax.

    ```sql
    -- Show tables
    SHOW TABLES;
    
    -- Query the weather_logs table
    SELECT * FROM weather_logs;

    -- Query Parquet file directly
    SELECT * FROM read_parquet('weather_data.parquet');
    ```

### Schedule Deployment

1. **Initialize your Prefect project (run once):**

    ```bash
    prefect init
    ```

    When prompted:

    ```bash
    ? Would you like to initialize your deployment configuration with a recipe? > local
    ```

    Choose `local` - this creates a `prefect.yaml` config file, sets up local storage for your flow code, and enables `prefect deploy`.

2. **Start the Prefect server**

    In a separate terminal, run:

    ```bash
    prefect server start
    ```

    This launches the local Prefect API and UI (accessible at http://127.0.0.1:4200).

3. **Use the CLI to create a scheduled deployment**

    Run the following command to deploy your flow with a cron schedule (here, every 10 minutes):

    ```bash
    prefect deploy \
    -n "Daily Weather Run" \
    --cron '*/10 * * * *' \
    --timezone "UTC"
    ```

    When prompted:

    ```bash
    ? Select a flow to deploy > weather_pipeline - main.py
    ```

    Confirm the flow to deploy.

4. **Create a work pool** (if prompted)

    If Prefect asks:

    ```bash
    ? Looks like you dont have any work pools this flow can be deployed to. Would you like to  create one? [y/n] (y): > y
    ```

    ```bash
    ? What infrastructure type would you like to use for your new work pool? > process
    ```

    ```bash
    ? Work pool name: > default-agent-pool
    ```

5. **Configure environment variable for the worker**

    Create a `.env` file in your project root with:

    ```ini
    PREFECT_API_URL=http://127.0.0.1:4200/api
    ```

    This points your worker to the local Prefect API server.

6. **Start a worker to pick up scheduled runs**

    Use a small Python script (`start_worker.py`) to load the .env and start the worker, then run:

    ```bash
    python start_worker.py
    ```

Your flow is now scheduled and will run according to your cron expression, executed by the worker connected to the local Prefect server.