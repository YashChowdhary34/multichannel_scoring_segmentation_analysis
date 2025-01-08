import requests
import pandas as pd
from kafka import KafkaProducer
import pymysql


API_URL = 'https://restcountries.com/v3.1/all'
producer = KafkaProducer(bootstrap_servers = 'localhost:9092')

DB_CONFIG = {
  'host': 'localhost',
  'user': 'root',
  'password': 'password',
  'database': 'retail_sales'
}

def extract_api_data():
  response = requests.get(API_URL)
  if response.status_code == 200:
    data = response.json()
    for item in data:
      producer.send('test', bytes(str(item), 'utf-8'))
    producer.flush()
    print('API data sent to Kafka!')

def extract_sql_data():
  connection = pymysql.connect(**DB_CONFIG)
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM raw_sales")

  for row in cursor.fetchall():
    producer.send('test', bytes(str(row), 'utf-8'))

  connection.close()
  producer.flush()
  print('SQL data sent to kafka!')

def extract_excel_data():
  df = pd.read_excel('./data/raw/online_retail.xlsx')
  for _, row in df.iterrows():
    producer.send('test', bytes(row.to_json(), 'utf-8'))
  producer.flush()
  print('CSV data sent to kafka!')


extract_excel_data()