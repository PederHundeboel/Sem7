from time import sleep

from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

value_schema = avro.load('/usr/src/app/schema/ValueSchema.avsc')
key_schema = avro.load('/usr/src/app/schema/KeySchema.avsc')
key = {"name": "loc"}
value = {"name": "Value", "favorite_number": 10, "favorite_color": "green", "age": 25}

avroProducer = AvroProducer(
    {'bootstrap.servers': 'kafka:19092', 'schema.registry.url': 'http://schema-registry:8082'},
    default_key_schema=key_schema, default_value_schema=value_schema
    )

for i in range(0, 50):
    value = {"name": "nguyen", "favorite_number": 10, "favorite_color": "green", "age": i}
    avroProducer.produce(topic='my_topic', value=value, key=key, key_schema=key_schema, value_schema=value_schema)
    sleep(0.01)
    print(i)

avroProducer.flush(10)