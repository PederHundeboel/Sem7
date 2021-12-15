from time import sleep

from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
import uuid


value_schema = avro.load('/usr/src/app/schema/ValueSchema2.avsc')
key_schema = avro.load('/usr/src/app/schema/KeySchema.avsc')
key = {"name": ""}
value = {"id":"someid","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[9.435367584228516,56.14679267047373],[9.473991394042967,56.14679267047373],[9.473991394042967,56.16075166204415],[9.435367584228516,56.16075166204415],[9.435367584228516,56.14679267047373]]]}}]}

avroProducer = AvroProducer(
    {'bootstrap.servers': 'kafka:19092', 'schema.registry.url': 'http://schema-registry:8082'},
    default_key_schema=key_schema, default_value_schema=value_schema
    )

for i in range(0, 20):
    key = uuid.uuid4().hex
    #value = {"name": "nguyen", "favorite_number": 10, "favorite_color": "green", "age": i}
    #avroProducer.produce(topic='products', value=value2, key={"name": str(i)}, key_schema=key_schema, value_schema=value_schema)
    avroProducer.produce(topic='products', value=value, key={"name": key}, key_schema=key_schema, value_schema=value_schema)
    sleep(0.01)
    print(i)

avroProducer.flush(10)

'''
{
    "name": "MyClass",
    "type": "record",
    "namespace": "com.acme.avro",
    "fields": [
      {
        "name": "type",
        "type": "string"
      },
      {
        "name": "features",
        "type": {
          "type": "array",
          "items": {
            "name": "features_record",
            "type": "record",
            "fields": [
              {
                "name": "type",
                "type": "string"
              },
              {
                "name": "properties",
                "type": {
                  "name": "properties",
                  "type": "record",
                  "fields": []
                }
              },
              {
                "name": "geometry",
                "type": {
                  "name": "geometry",
                  "type": "record",
                  "fields": [
                    {
                      "name": "type",
                      "type": "string"
                    },
                    {
                      "name": "coordinates",
                      "type": {
                        "type": "array",
                        "items": {
                          "type": "array",
                          "items": {
                            "type": "array",
                            "items": "float"
                          }
                        }
                      }
                    }
                  ]
                }
              }
            ]
          }
        }
      }
    ]
  }
'''