from kafka_producer import KafkaProducerWrapper

# IPv6-Adresse im Format [addr]:port
producer = KafkaProducerWrapper("[fd00:dead:cafe::10]:9092", "order")
producer.send_message("Hallo Kafka über IPv6!")
