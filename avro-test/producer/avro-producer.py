from time import sleep

from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
import uuid
import json

value_schema = avro.load('/usr/src/app/schema/ValueSchema4.avsc')
key_schema = avro.load('/usr/src/app/schema/KeySchema.avsc')
key = {"name": ""}

with open("/usr/src/app/features.json") as jsonFile:
    #jsonObject = json.load(jsonFile)
    value = {"geojson": str(jsonFile.read())}

avroProducer = AvroProducer(
    {'bootstrap.servers': 'kafka:19092', 'schema.registry.url': 'http://schema-registry:8082', 'compression.type': 'snappy', 'message.max.bytes': 15728640},
    default_key_schema=key_schema, default_value_schema=value_schema
    )

for i in range(0, 1):
    key = uuid.uuid4().hex
    #value = {"name": "nguyen", "favorite_number": 10, "favorite_color": "green", "age": i}
    #avroProducer.produce(topic='products', value=value2, key={"name": str(i)}, key_schema=key_schema, value_schema=value_schema)
    avroProducer.produce(topic='products', value=value, key={"name": key}, key_schema=key_schema, value_schema=value_schema)
    sleep(0.01)
   # print(i)

avroProducer.flush()