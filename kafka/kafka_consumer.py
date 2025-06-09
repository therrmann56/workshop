from confluent_kafka import Consumer

class KafkaConsumerWrapper:
    def __init__(self, bootstrap_servers: str, topic: str, group_id: str):
        self.topic = topic
        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        })
        self.consumer.subscribe([self.topic])

    def receive(self):
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    print(f'? Consumer error: {msg.error()}')
                    continue
                print(f'?? Received: {msg.value().decode("utf-8")}')
        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()
