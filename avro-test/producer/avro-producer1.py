import json
#from bson import json_util
from confluent_kafka import Producer
from kafka import KafkaProducer
from kafka.errors import KafkaError
import uuid

#producer = KafkaProducer(bootstrap_servers='kafka:19092')
#producer = KafkaProducer(bootstrap_servers='kafka:19092', value_serializer=lambda m: json.dumps(m).encode('utf-8'))
p = Producer({'bootstrap.servers': 'kafka:19092'})

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))

with open("/usr/src/app/features.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    key = uuid.uuid4().hex
    p.produce('products', key=key, value=json.dumps(jsonObject), callback=acked)
    # Wait up to 1 second for events. Callbacks will be invoked during
    # this method call if the message is acknowledged.
    #p.poll(1)
    p.flush()
    jsonFile.close()

#producer.send('products', jsonObject).add_callback(on_send_success).add_errback(on_send_error)