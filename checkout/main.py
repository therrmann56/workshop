import json
import time
import uuid
from datetime import datetime
from confluent_kafka import Producer

# Konfiguration (angepasst auf IPv6 Setup)
conf = {
    'bootstrap.servers': '[fd00:dead:cafe::10]:9092',
    'client.id': 'checkout-producer'
}

producer = Producer(conf)

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
        "status": "pending",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

def delivery_report(err, msg):
    if err is not None:
        print(f"? Delivery failed: {err}")
    else:
        print(f"? Delivered to {msg.topic()} [{msg.partition()}]")

print("?? Starte Checkout Producer...")

try:
    while True:
        event = create_checkout_event()
        producer.produce(
            topic="checkout",
            key=event["checkout_id"],
            value=json.dumps(event),
            callback=delivery_report
        )
        producer.poll(0)
        time.sleep(0.3)
except KeyboardInterrupt:
    print("? Producer gestoppt.")
finally:
    producer.flush()