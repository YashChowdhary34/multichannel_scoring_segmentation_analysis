from kafka import KafkaConsumer
import pymysql
import json
import logging 

TOPIC = 'transformed_data_stream'
BROKER = 'localhost:9092'

DF_FILE = 'retail_sales.db'
TABLE_NAME = 'transformed_sales'
DB_CONFIG = {
  'host': 'localhost',
  'user': 'root',
  'password': 'password',
  'database': 'retail_sales'
}

LOG_FILE = 'loading_pipeline.log'
logging.basicConfig(
  filename=LOG_FILE,
  level=logging.INFO,
  format='%(asctime)s - %(levelname)s - %(message)s'
)

def initialize_database():
  connection = pymysql.connect(**DB_CONFIG)
  cursor = connection.cursor()

  cursor.execute(f"""
                  CREATE TABLE IF NOT EXISTS transformed_sales (
                 source VARCHAR(15),
                 processed_at VARCHAR(25),
                 InvoiceNo	VARCHAR(15),
                 StockCode	VARCHAR(15),
                 Description	VARCHAR(50),
                 Quantity	INT,
                 InvoiceDate	DATE,
                 UnitPrice	FLOAT,
                 CustomerID	FLOAT,
                 Country  VARCHAR(25)
                 )
                 """)
  connection.commit()
  connection.close()
  logging.info("DB initialized")

def insert_into_database(data):
  try:
    connection = pymysql.connect(**DB_CONFIG)
    cursor = connection.cursor()

    source = data.get("source")
    processed_at = data.get("processed_at")
    invoice_no = data.get("InvoiceNo")
    stock_code = data.get("StockCode") 
    description = data.get("Description") 
    quantity = data.get("Quantity") 
    invoice_date = data.get("InvoiceDate") 
    unit_price = data.get("UnitPrice") 
    customer_id = data.get("CustomerID") 
    country = data.get("Country")

    query = """
                INSERT INTO transformed_sales (InvoiceNo, StockCode, Description, Quantity,
                                              InvoiceDate, UnitPrice CustomerID, Country)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
    
    cursor.execute(query, (source, processed_at, invoice_no, stock_code, description, quantity,
                          invoice_date, unit_price, customer_id, country))
    
    connection.commit()
    connection.close()
    logging.info(f'Inserted data into db: {data}')

  except Exception as e:
    logging.error(f'Error inserting data into db: {e}, data: {data}')


consumer = KafkaConsumer(
  TOPIC,
  bootstrap_server=BROKER,
  auto_offset_reset='earliest',
  enable_auto_commit=TRUE,
  value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

logging.info(f'Started consuming from topic: {TOPIC}')

initialize_database()
for message in consumer:
  transformed_data = message.value
  logging.info(f'Received transformed data: {transformed_data}')

  try:
    insert_into_database(transformed_data)
  except Exception as e:
    logging.error(f'Error processing message: {e}, Data: {transformed_data}')