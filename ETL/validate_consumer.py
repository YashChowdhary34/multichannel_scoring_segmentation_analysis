from kafka import KafkaConsumer

TOPIC = 'test'
BROKER = 'localhost:9092'

consumer = KafkaConsumer(
  TOPIC,
  bootstrap_servers = BROKER,
  enable_auto_commit = True,
  value_deserializer = lambda x: x.decode('utf-8')
)

print(f'Cunsuming messages from Kafka topic: {TOPIC}\n')

for message in consumer:
  print(f'Received message: {message.value}')
  break