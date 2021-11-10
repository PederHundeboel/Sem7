from kafka import KafkaConsumer
from kafka import KafkaProducer
from json import loads
import happybase
import json
import secrets
import time
from downloader import Downloader

def getConsumer():
    consumer = KafkaConsumer(
        'download-requests',
        bootstrap_servers=['kafka:19092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='download-group',
        value_deserializer=lambda x: loads(x.decode('utf-8')))
    return consumer

consumer = None

while consumer == None:
    try:
        consumer = getConsumer()
    except:
        print('couldnt establish consumer, sleeping and retrying in 5 seconds')
        time.sleep(5)


#hb_connection = happybase.Connection('hbase', 9037)



producer = KafkaProducer(bootstrap_servers=['kafka:19092'],
                         value_serializer=lambda x:
                         json(x).encode('utf-8'))

sentinelDownloader = Downloader(secrets.USER, secrets.PASSWORD, None)


for msg in consumer:
    msg = msg.value
    res = sentinelDownloader.query(msg)
    producer.send('processing-requests', value=res)
