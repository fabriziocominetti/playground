# Wikipedia Live Monitoring with Apache Kafka

A simple real-time data engineering project that streams live Wikipedia edits through Apache Kafka into a PostgreSQL database and a monitor alert system.

## Features
- **Real-time Streaming:** Consumes from the official Wikipedia SSE stream.
- **Message Broker:** Uses Apache Kafka (KRaft mode) to decouple producers and consumers.
- **Data Persistence:** Automatically stores all edits into a PostgreSQL database.
- **Alert System:** Monitors the stream for "Large Edits" (>500 characters) in real-time.
- **Observability:** Centralized logging to `pipeline.log` and web dashboards for Kafka and Postgres.

## Tech Stack
- **Apache Kafka** (via Docker)
- **PostgreSQL** (via Docker)
- **Python 3.x**
- **Docker & Docker Compose**

## Setup

1. **Install Python Dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

2. **Start Infrastructure:**
   Ensure Docker Desktop is running, then start the containers:
   ```powershell
   docker-compose up -d
   ```

## Launch Sequence

Run each of these in a separate terminal window:

1. **Start the Producer:** (Wikipedia -> Kafka)
   ```powershell
   python producer.py
   ```

2. **Start the DB Consumer:** (Kafka -> PostgreSQL)
   ```powershell
   python db_consumer.py
   ```

3. **Start the Alert Monitor:** (Kafka -> Terminal Alerts)
   ```powershell
   python consumer.py
   ```

## Monitoring Dashboards
- **Kafka-UI:** [http://localhost:8080](http://localhost:8080) (View topics and messages)
- **pgAdmin:** [http://localhost:5050](http://localhost:5050) (Manage database)
  - Login: `admin@admin.com` / `admin`
  - Host: `db` (internal) or `localhost` (external)

## How to Stop
1. `Ctrl+C` in all Python terminals.
2. Stop infrastructure:
   ```powershell
   docker-compose down
   ```
