from confluent_kafka import Producer

class KafkaProducerWrapper:
    def __init__(self, bootstrap_servers: str, topic: str):
        self.topic = topic
        self.producer = Producer({'bootstrap.servers': bootstrap_servers})

    def send_message(self, message: str):
        def delivery_report(err, msg):
            if err is not None:
                print(f'? Delivery failed: {err}')
            else:
                print(f'? Message delivered to {msg.topic()} [{msg.partition()}]')

        self.producer.produce(self.topic, message.encode('utf-8'), callback=delivery_report)
        self.producer.flush()
