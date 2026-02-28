import json
import logging
import requests
from kafka import KafkaProducer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - PRODUCER - %(message)s',
    handlers=[logging.FileHandler("pipeline.log"), logging.StreamHandler()]
)

# Setup the Kafka producer
try:
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        acks=1 # Ensure at least one broker receives the message
    )
except Exception as e:
    logging.error(f"Failed to connect to Kafka: {e}")
    exit(1)

WIKI_STREAM_URL = 'https://stream.wikimedia.org/v2/stream/recentchange'
TOPIC_NAME = 'wiki-edits'

logging.info(f"Connecting to Wikipedia stream: {WIKI_STREAM_URL}")

def run_producer():
    try:
        # Wikipedia requires a descriptive User-Agent header
        headers = {
            'User-Agent': 'KafkaStreamLearningProject/1.0 (Contact: your-email@example.com)'
        }
        
        # We'll use a manual line-by-line reader to be 100% sure we handle the stream
        response = requests.get(WIKI_STREAM_URL, stream=True, timeout=10, headers=headers)
        
        if response.status_code != 200:
            logging.error(f"Failed to connect to Wikipedia. Status Code: {response.status_code}")
            return

        logging.info("Connection established. Listening for events...")

        current_event = None
        for line in response.iter_lines():
            if not line:
                continue
            
            line_str = line.decode('utf-8')
            
            # SSE format: "data: { ... }"
            if line_str.startswith('data: '):
                try:
                    data_str = line_str[6:] # Strip "data: "
                    change = json.loads(data_str)
                    
                    if change.get('type') == 'edit':
                        data_to_send = {
                            'user': change.get('user'),
                            'title': change.get('title'),
                            'wiki': change.get('server_name'),
                            'length_change': change.get('length', {}).get('new', 0) - change.get('length', {}).get('old', 0),
                            'timestamp': change.get('timestamp')
                        }
                        
                        # Send to Kafka
                        producer.send(TOPIC_NAME, value=data_to_send)
                        logging.info(f"Sent edit: {data_to_send['title']} by {data_to_send['user']}")
                
                except json.JSONDecodeError:
                    continue
                except Exception as e:
                    logging.error(f"Error processing line: {e}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Stream connection error: {e}")
    except KeyboardInterrupt:
        logging.info("Producer stopped by user.")
    finally:
        producer.close()
        logging.info("Kafka producer closed.")

if __name__ == "__main__":
    run_producer()
