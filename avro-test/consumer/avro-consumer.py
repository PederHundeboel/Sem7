from confluent_kafka import KafkaError
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
from confluent_kafka.cimpl import TopicPartition

c = AvroConsumer(
    {'bootstrap.servers': 'kafka:19092', 'group.id': 'cgroudid-2', 'schema.registry.url': 'http://schema-registry:8082',
     "api.version.request": True})
c.subscribe(['my_topic'])
running = True
while running:
    msg = None
    try:
        msg = c.poll(10)
        if msg:
            if not msg.error():
                print(msg.value())
                print(msg.key())
                print(msg.partition())
                print(msg.offset())
                c.commit(msg)
            elif msg.error().code() != KafkaError._PARTITION_EOF:
                print(msg.error())
                running = False
        else:
            print("No messages..")
    except SerializerError as e:
        print("Failed readig message %s: %s" % (msg, e))
        running = False
c.commit()
c.close()