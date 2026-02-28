import psycopg2
import json
import logging
import psycopg2
from kafka import KafkaConsumer

# setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="wikipedia_stats",
        user="wiki_user",
        password="wiki_pass"
    )

# create the table if it doesn't exists
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
                CREATE TABLE IF NOT EXISTS edits (
                id SERIAL PRIMARY KEY,
                wiki TEXT,
                title TEXT,
                user_name TEXT,
                length_change INTEGER,
                timestamp_str TEXT
                )
                ''')
    conn.commit()
    cur.close()
    conn.close()
    logging.info("Database initialized successfully.")

# main consumer loop
def run_consumer():
    consumer = KafkaConsumer(
        'wiki-edits',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        group_id='db-storage-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    init_db()
    conn = get_db_connection()
    cur = conn.cursor()

    logging.info("Starting Kafka -> Postgres consumer")

    try:
        for message in consumer:
            edit = message.value
            # insert into database
            cur.execute(
                "INSERT INTO edits (wiki, title, user_name, length_change, timestamp_str) VALUES (%s, %s, %s, %s, %s)",
                (edit['wiki'], edit['title'], edit['user'], edit['length_change'], str(edit['timestamp']))
            )
            conn.commit()

            logging.info(f"Saved to DB: {edit['title']} by {edit['user']}")
    except Exception as e:
        logging.error(f"Error in consumer: {e}")
    finally:
        cur.close()
        conn.close()
        consumer.close()

if __name__ == "__main__":
    run_consumer()
