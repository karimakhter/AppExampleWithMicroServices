import json
import logging

from kafka import KafkaConsumer

logger = logging.getLogger('producer')
try:
    consumer = KafkaConsumer( 'testtopic', bootstrap_servers=['kafka:9092'] )
    logger.info( "Start Consuming" )
    for mes in consumer:
        print( f"Topic : {mes.topic} Key : {mes.key.decode( 'utf-8' )} Message : {mes.value.decode( 'utf-8' )}" )
        data = json.loads( mes.value.decode( 'utf-8' ) )
except:
    logger.warning( "Consumer unable to connect to borker" )