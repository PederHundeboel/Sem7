from kafka import KafkaConsumer
from json import loads
from downloader import download as d

consumer = KafkaConsumer(
    'downloads',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8')))

while consumer.bootstrap_connected():
    for e in consumer:
        d(e)
