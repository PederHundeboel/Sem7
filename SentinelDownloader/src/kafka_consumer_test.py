import kafka
from kafka import KafkaConsumer
from json import loads

def getConsumer():
    consumer = KafkaConsumer(
        'processing-requests',
        bootstrap_servers=['localhost:9992'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='processing-requests',
        value_deserializer=lambda x: loads(x.decode('utf-8')))
    return consumer



consumer = getConsumer()



for msg in consumer:
    msg = msg.value
    print('a message was recieved from kafka: ' + msg)

