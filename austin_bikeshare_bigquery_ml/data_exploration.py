from google.cloud import bigquery
from dotenv import load_dotenv
import os

load_dotenv()
PROJECT = os.getenv('PROJECT')

# Initialize BigQuery client and project
client = bigquery.Client(project=PROJECT)

# Define the query
query = """
SELECT *
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
LIMIT 5
"""

# Execute the query
print("Executing query...")
query_job = client.query(query) # Make an API request

# Get the results
print("Query executed.")
results = query_job.result()

# Convert results to a pandas DataFrame
table = results.to_dataframe()
print(table)
print(table.columns)

print("---")

# The distinct subscriber types.

query_distinct_subscriber_types = """
SELECT
    DISTINCT subscriber_type,
    COUNT(*) as count
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
GROUP BY subscriber_type
"""

print("Executing query...")
query_job = client.query(query_distinct_subscriber_types)

print("Query executed.")
results = query_job.result()

# Iterate through results
for row in results:
    print(f"Subscriber Types: {row.subscriber_type} - Count: {row.count}")

print("---")

# The number of distinct start stations.

query_count_start_stations = """
SELECT COUNT(DISTINCT start_station_name) as start_station_count
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
"""

print("Executing query...")
query_job = client.query(query_count_start_stations)

print("Query executed.")
results = query_job.result()

# Iterate through results
for row in results:
    print(f"Start Station Count: {row.start_station_count}")

print("---")

# The number of distinct end stations.

query_count_end_stations = """
SELECT COUNT(DISTINCT end_station_name) as end_station_count
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
"""

print("Executing query...")
query_job = client.query(query_count_end_stations)

print("Query executed.")
results = query_job.result()

# Iterate through results
for row in results:
    print(f"End Station Count: {row.end_station_count}")

print("---")

# The distinct bike types.

query_distinct_bike_types = """
SELECT
    DISTINCT bike_type,
    COUNT(*) as count
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
GROUP BY bike_type
"""

print("Executing query...")
query_job = client.query(query_distinct_bike_types)

print("Query executed.")
results = query_job.result()

# Iterate through results
for row in results:
    print(f"Bike Type: {row.bike_type} - Count: {row.count}")

print("---")

# The total count of trips.
# The average duration of trips.

query_total_trips_avg_duration = """
SELECT COUNT(*) as total_trips,
       AVG(duration_minutes) as avg_duration
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
"""

print("Executing query...")
query_job = client.query(query_total_trips_avg_duration)

print("Query executed.")
results = query_job.result()

for row in results:
    print(f"Total Trips: {row.total_trips}")
    print(f"Average Duration: {row.avg_duration:.2f} minutes")

print("---")

# The top 5 most popular start stations.

query_top_5_start_stations = """
SELECT COUNT(*) as total_trips,
       AVG(duration_minutes) as avg_duration,
       start_station_id,
       start_station_name
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
GROUP BY start_station_id, start_station_name
ORDER BY total_trips DESC
LIMIT 5
"""

print("Executing query...")
query_job = client.query(query_top_5_start_stations)

print("Query executed.")
results = query_job.result()

for row in results:
    print(f"Total Trips: {row.total_trips}")
    print(f"Average Duration: {row.avg_duration:.2f} minutes")
    print(f"Start Station ID: {row.start_station_id}")
    print(f"Start Station Name: {row.start_station_name}")

print("---")

# The 3 busiest hours of the day for bike rentals.

query_busiest_hours = """
SELECT EXTRACT(HOUR FROM start_time) as hour,
       COUNT(*) as total_trips
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
GROUP BY hour
ORDER BY total_trips DESC
LIMIT 3
"""

print("Executing query...")
query_job = client.query(query_busiest_hours)

print("Query executed.")
results = query_job.result()

for row in results:
    print(f"Hour: {row.hour}")
    print(f"Total Trips: {row.total_trips}")

print("---")

# Who rides for longer between 'Walk-up' vs 'Annual Member' subscribers.

query_who_rides_longer = """
SELECT subscriber_type,
    COUNT(*) as total_trips,
    AVG(duration_minutes) as avg_duration
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
WHERE subscriber_type IN ('Walk Up', 'Annual Member')
GROUP BY subscriber_type
ORDER BY total_trips DESC
"""

print("Executing query...")
query_job = client.query(query_who_rides_longer)

print("Query executed.")
results = query_job.result()

for row in results:
    print(f"Subscriber Type: {row.subscriber_type}")
    print(f"Total Trips: {row.total_trips}")
    print(f"Average Duration: {row.avg_duration:.2f} minutes")

print("---")

# Top 5 most frequent routes (start station to end station).

query_top_5_routes = """
SELECT start_station_name,
    end_station_name,
    COUNT(*) as total_trips
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
GROUP BY start_station_name, end_station_name
ORDER BY total_trips DESC
LIMIT 5
"""

print("Executing query...")
query_job = client.query(query_top_5_routes)

print("Query executed.")
results = query_job.result()

for row in results:
    print(f"Start Station: {row.start_station_name}")
    print(f"End Station: {row.end_station_name}")
    print(f"Total Trips: {row.total_trips}")

# Bike usage on weekends vs weekdays.

query_weekend_weekday = """
SELECT
    CASE
        WHEN EXTRACT(DAYOFWEEK FROM start_time) IN (6, 7) THEN 'Weekend' -- 6 = Saturday, 7 = Sunday
        ELSE 'Weekday'
    END as day_type,
    COUNT(*) as total_trips
FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
GROUP BY day_type
"""

print("Executing query...")
query_job = client.query(query_weekend_weekday)

print("Query executed.")
results = query_job.result()

for row in results:
    print(f"Day Type: {row.day_type}")
    print(f"Total Trips: {row.total_trips}")