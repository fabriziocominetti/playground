import json
import logging
from kafka import KafkaConsumer


# setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - MONITOR - %(message)s',
    handlers=[logging.FileHandler("pipeline.log"), logging.StreamHandler()]
)


# setup the Kafka consumer
consumer = KafkaConsumer(
    'wiki-edits', # the topic to listen to
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    group_id='wiki-monitor-group', # it works like a bookmark
    value_deserializer=lambda m: json.loads(m.decode('utf-8')) # bytes back to dict
)

logging.info("Monitoring Wikipedia for large edits (>500 chars)")

try:
    # infinite loop to listen for new messages
    for message in consumer:
        edit = message.value
        # detect big changes
        change_size = abs(edit['length_change'])
        if change_size > 500:
            logging.warning(f"--- LARGE EDIT DETECTED --- Wiki: {edit['wiki']} | Page: {edit['title']} | User: {edit['user']} | Size: {edit['length_change']}")
        else:
            logging.info(f"Normal edit on {edit['title']} ({edit['wiki']})")
except KeyboardInterrupt:
    logging.info("Consumer stopped.")
finally:
    consumer.close()
