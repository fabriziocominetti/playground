from sqlalchemy import exc
import sqlalchemy
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import sqlalchemy
from sqlalchemy.types import String


# Connection configuration
DB_USER = "sa"
DB_PASS = "Sportlake!2026"
DB_HOST = "127.0.0.1"
DB_PORT = "1433"

DRIVER = "ODBC Driver 17 for SQL Server"

# Connect to the default 'master' database to create the DB
master_url = f"mssql+pyodbc://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/master?driver={DRIVER}"
master_engine = sqlalchemy.create_engine(master_url, isolation_level="AUTOCOMMIT")

with master_engine.connect() as conn:
    try:
        conn.execute(sqlalchemy.text("CREATE DATABASE sportlake_db"))
        print("Database 'sportlake_db' created successfully!")
    except Exception as e:
        print("Error during database creation:", str(e).split('\n')[0])

# Connect to the new 'sportlake_db' databse
db_url = f"mssql+pyodbc://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/sportlake_db?driver={DRIVER}"
engine = sqlalchemy.create_engine(db_url)

# Setup Faker
fake = Faker('it_IT')
Faker.seed(1899)
random.seed(1899)

print("Generating synthetic data")

# --- Customers Data ---
num_customers = 500
customers = []
membership_tiers = ["Cuore Rossonero", "Web Registered", "Season Ticket - VIP", "Season Ticket - Standard"]

for i in range(1, num_customers + 1):
    customers.append({
        "customer_id": i,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "city": fake.city(),
        "membership_tier": random.choices(membership_tiers, weights=[40, 30, 5, 25])[0],
        "join_date": fake.date_between(start_date='-5y', end_date='today')
    })
df_customers = pd.DataFrame(customers)

# --- Ticketing Data ---
sectors = ["Curva Sud", "Tribuna Rossa", "Primo Anello Verde", "Secondo Anello Arancio"]
ticketing = []
for i in range(1, 1500):
    ticketing.append({
        "ticket_id": 10000 + i,
        "customer_id": random.randint(1, num_customers),
        "match_name": "AC Milan vs Inter",
        "match_date": fake.date_between(start_date='today', end_date='+2m'),
        "sector": random.choices(sectors, weights=[40, 10, 25, 25])[0],
        "price": round(random.uniform(40.0, 250.0), 2)
    })
df_ticketing = pd.DataFrame(ticketing)

# --- eCommerce Data ---
products = ["Home Jersey 2026", "Away Jersey", "Retro Scarf", "Milan Cap", "Mug"]
ecommerce = []
for i in range(1, 800):
    ecommerce.append({
        "order_id": 50000 + i,
        "customer_id": random.randint(1, num_customers),
        "order_date": fake.date_between(start_date='-1y', end_date='today'),
        "product_name": random.choices(products, weights=[30, 20, 15, 25, 10])[0],
        "total_amount": round(random.uniform(15.0, 130.0), 2)
    })
df_ecommerce = pd.DataFrame(ecommerce)

# Convert dates to strings to bypass the legacy driver limitation
df_customers['join_date'] = df_customers['join_date'].astype(str)
df_ticketing['match_date'] = df_ticketing['match_date'].astype(str)
df_ecommerce['order_date'] = df_ecommerce['order_date'].astype(str)

print("Loading data into SQL Server")

# Helper to limit string sizes to 255 chars for the legacy driver
def map_strings(df):
    return {col: String(255) for col in df.select_dtypes(include=['object']).columns}

# Write Dataframes to SQL Server tables
try:
    df_customers.to_sql(
        'raw_customers', 
        engine, 
        if_exists='replace', 
        index=False, 
        dtype=map_strings(df_customers)
    )
    print("Customers table loaded")

    df_ticketing.to_sql(
        'raw_ticketing', 
        engine, 
        if_exists='replace', 
        index=False, 
        dtype=map_strings(df_ticketing)
    )
    print("Ticketing table loaded")

    df_ecommerce.to_sql(
        'raw_ecommerce', 
        engine, 
        if_exists='replace', 
        index=False, 
        dtype=map_strings(df_ecommerce)
    )
    print("eCommerce table loaded")

    print("All data ingested successfully!")

except Exception as e:
    print("Error saving to database:", str(e).split('\n')[0])
