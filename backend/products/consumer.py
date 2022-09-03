import json

from kafka import KafkaConsumer
def json_serliazer(data):
    return json.dumps(data).encode('utf-8')


print("Start Consuming")

try:
    consumer = KafkaConsumer(bootstrap_servers=['kafka:9092'], topic='testtopic')
    print(consumer)
except:
    print("Conusmer unable to connect with broker")