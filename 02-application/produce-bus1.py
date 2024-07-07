import logging
import os
import json
import uuid
import time
from kafka import KafkaProducer
from datetime import datetime

#INIT KAFKA PRODUCER

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KafkaProducer")

# Configuration from environment variables
TOPIC = os.getenv('TOPIC', 'busdata')
#MESSAGE_COUNT = int(os.getenv('MESSAGE_COUNT', 100))
#MESSAGE = os.getenv('MESSAGE', 'Hello-world')
PRODUCER_ACKS = os.getenv('PRODUCER_ACKS', 'all')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Set the logging level
logger.setLevel(getattr(logging, LOG_LEVEL.upper()))

producer = KafkaProducer(
    bootstrap_servers='172.20.255.240:9094', # Replace with svc Kafka external address `dev-cluster-kafka-external-bootstrap`
    acks=PRODUCER_ACKS,
    key_serializer=str.encode,
    value_serializer=str.encode
)

#LOAD DATA FROM JSON FILE
input_file = open('./data/bus1.json')
json_array = json.load(input_file)
coordinates = json_array['features'][0]['geometry']['coordinates']

#GENERATE UUID
def generate_uuid():
    return uuid.uuid4()

#CONSTRUCT MESSAGE AND SEND IT TO KAFKA
data = {}
data['busline'] = '00001'

def generate_checkpoint(coordinates):
    i = 0
    while i < len(coordinates):
        data['key'] = data['busline'] + "_" + str(generate_uuid())
        data['timestamp'] = str(datetime.now().isoformat())
        data['latitude'] = coordinates[i][1]
        data['longitude'] = coordinates[i][0]
        message = json.dumps(data)
        producer.send(TOPIC, key=data['key'], value=message)
        logger.info(f'Sent message {i+1} to topic {TOPIC}')
        time.sleep(2)
        #if bus reaches the end of the route, start from the beginning
        if i == len(coordinates) - 1:
            i = 0
        else:
            i += 1

generate_checkpoint(coordinates)

producer.flush()
producer.close()
logger.info('Finished producing messages')
