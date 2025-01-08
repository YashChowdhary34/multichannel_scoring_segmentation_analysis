from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers = 'localhost:9092')
producer.send('test', b'Test message from producer')
producer.flush()
print('Message sent successfully!')