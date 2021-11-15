from time import sleep

from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

value_schema = avro.load('/usr/src/app/schema/ValueSchema.avsc')
key_schema = avro.load('/usr/src/app/schema/KeySchema.avsc')
key = {"name": ""}
value = {"name": "Value", "favorite_number": 10, "favorite_color": "green", "age": 25}
value2 = {"name" : "test_meter", "type" : "meter", "timestamp" : 1574667646013, "dimensions" : {"dimensions1" : "InstanceID","dimensions2" : "i-aaba32d4"},"values" : {"count" : 32423.0,"oneMinuteRate" : 342342.2,"fiveMinuteRate" : 34234.2,"fifteenMinuteRate" : 2123123.1,"meanRate" : 2312312.1}}

avroProducer = AvroProducer(
    {'bootstrap.servers': 'kafka:19092', 'schema.registry.url': 'http://schema-registry:8082'},
    default_key_schema=key_schema, default_value_schema=value_schema
    )

for i in range(0, 20):
    #value = {"name": "nguyen", "favorite_number": 10, "favorite_color": "green", "age": i}
    avroProducer.produce(topic='products', value=value2, key={"name": str(i)}, key_schema=key_schema, value_schema=value_schema)
    sleep(0.01)
    print(i)

avroProducer.flush(10)