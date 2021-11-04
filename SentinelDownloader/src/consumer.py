from kafka import KafkaConsumer
from kafka import KafkaProducer
from json import loads
import happybase
import json
import secrets
from downloader import Downloader

hb_connection = happybase.Connection('hbase', 9037)

consumer = KafkaConsumer(
    'download-requests',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='download-group',
    value_deserializer=lambda x: loads(x.decode('utf-8')))

producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
                         value_serializer=lambda x:
                         json(x).encode('utf-8'))

sentinelDownloader = Downloader(secrets.USER, secrets.PASSWORD, hb_connection)


for msg in consumer:
    msg = msg.value
    res = sentinelDownloader.query(msg)
    producer.send('processing-requests', value=res)
