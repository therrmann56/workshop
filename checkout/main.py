import json
import time
import uuid
import random
from datetime import datetime
from confluent_kafka import Producer, KafkaException, Consumer


# Konfiguration (angepasst auf IPv6 Setup)
pconf = {
    'bootstrap.servers': '[fd00:dead:cafe::10]:9092',
    'client.id': 'checkout-producer'
}


cconf = {
    'bootstrap.servers': '[fd00:dead:cafe::10]:9092',
    'group.id': 'checkout-group',
    'auto.offset.reset': 'latest'
}

producer = Producer(pconf)
consumer = Consumer(cconf)
consumer.subscribe(['checkout'])

count = 0

def create_checkout_event():
    return {
        "checkout_id": str(uuid.uuid4()),
        "user_id": str(uuid.uuid4()),
        "cart_items": [
            {"product_id": "sku-123", "quantity": 1, "price": 49.99},
            {"product_id": "sku-456", "quantity": 2, "price": 19.99}
        ],
        "total_amount": 89.97,
        "currency": "EUR",
        "payment_method": "credit_card",
        "shipping_address": {
            "name": "Max Mustermann",
            "street": "Musterstra�e 1",
            "zip": "12345",
            "city": "Musterstadt",
            "country": "DE"
        },
        "status": "created",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

def delivery_report(err, msg):
    if err is not None:
        print(f"? Delivery failed: {err}")
    else:
        print(f"? Delivered to {msg.topic()} [{msg.partition()}]")

def processConsumer():

    msg = consumer.poll(1.0)
    if msg is None:
        return

    payload = json.loads(msg.value().decode('utf-8'))
    print(f"📦 Empfangen: {payload}")

    changestatus(payload)


def changestatus(payload):

    if payload['status'] == 'CheckoutSubmitted':
        return

    if payload['status'] == 'created':
        payload['status'] = 'AddressSubmitted'
    elif payload['status'] == 'AddressSubmitted':
        payload['status'] = 'PaymentMethodSubmitted'
    elif payload['status'] == 'PaymentMethodSubmitted':
        payload['status'] = 'CheckoutSubmitted'
        if random.randint(1, 100) > 7:
            return

    submitMsg(payload)

def submitMsg(payload):
    print(f"📦 New Payload: {payload}")
    producer.produce(
        topic="checkout",
        key=event["checkout_id"],
        value=json.dumps(payload),
        callback=delivery_report
    )


print("?? Starte Checkout Producer...")
print("✅ Warte auf Kafka-Nachrichten im Topic 'checkout'...")

try:
    while True:
        event = create_checkout_event()
        producer.produce(
            topic="checkout",
            key=event["checkout_id"],
            value=json.dumps(event),
            callback=delivery_report
        )
        #producer.poll(0)
        time.sleep(0.3)

        processConsumer()
except KeyboardInterrupt:
    print("? Producer gestoppt.")
finally:
    producer.flush()