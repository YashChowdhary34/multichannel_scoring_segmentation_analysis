from kafka import KafkaProducer, KafkaConsumer
import json
import logging
from datetime import datetime

INPUT_TOPIC = 'test'
OUTPUT_TOPIC = 'transformed_data_stream'
BROKER = 'localhost:9092'

LOG_FILE = 'transformation_pipeline.log'
logging.basicConfig(
  filename=LOG_FILE,
  level=logging.INFO,
  format='%(asctime)s - %(levelname)s - %(message)s'
)

def transform_data(raw_data):
  try:
    transformed_data = raw_data if isinstance(raw_data, dict) else {'raw': raw_data}
    transform_data['source'] = transform_data.get('source', 'unknown')
    transform_data['processed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return transformed_data
  except Exception as e:
    logging.error(f'Error during transformation: {e}, Data: {raw_data}')

consumer = KafkaConsumer(
  INPUT_TOPIC,
  bootstrap_servers=BROKER,
  auto_offset_reset='earliest',
  enable_auto_commit=True,
  value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)
logging.info(f"Started consuming from topic: {INPUT_TOPIC}")

for message in consumer:
    raw_data = message.value
    logging.info(f"Received data: {raw_data}")

    try:
        transformed_data = transform_data(raw_data)

        if transformed_data:
            producer.send(OUTPUT_TOPIC, transformed_data)
            logging.info(f"Sent transformed data: {transformed_data}")
        else:
            logging.warning(f"Skipping invalid data: {raw_data}")

    except Exception as e:
        logging.error(f"Error processing message: {e}, Data: {raw_data}")

producer.flush()
logging.info(f"All transformed data sent to topic: {OUTPUT_TOPIC}")