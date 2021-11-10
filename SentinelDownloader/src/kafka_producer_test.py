import sys

from kafka import KafkaProducer
from json import dumps
from pathlib import Path

def getProducer():
    producer = KafkaProducer(bootstrap_servers=['localhost:9992'],
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
    return producer

producer = None
producer = getProducer()


args = sys.argv

txt = Path('g1.geojson').read_text()
txt = txt.replace('\n', '')

producer.send('download-requests', value=txt)
