import json
import logging

logger = logging.getLogger('producer')
from kafka import KafkaProducer


def publish( data, method ):
    try:
        producer = KafkaProducer( bootstrap_servers=['kafka:9092'] )
        producer.send( 'testtopic', key=method, value=json.dumps( data ).encode( 'utf-8' ) )
        producer.flush()
    except:
        logger.warning("Producer Unable to connnect to broker")

