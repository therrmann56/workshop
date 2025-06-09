from kafka_consumer import KafkaConsumerWrapper

consumer = KafkaConsumerWrapper("[fd00:dead:cafe::10]:9092", "checkout", "ipv6-consumer-group")
print(consumer.receive())
