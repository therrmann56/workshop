# filter/main.py
# Dieses Skript liest Logzeilen ein und filtert nur Zeilen mit dem Statuscode 200.

import json
import uuid
from datetime import datetime
from confluent_kafka import Producer, Consumer, KafkaException
from sqlalchemy import create_engine, Column, String, Integer, DECIMAL, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from checkout.main import delivery_report

Base = declarative_base()

DB_URI = 'mysql+pymysql://user:userpw@[fd00:dead:cafe::100]:3306/analytics'
engine = create_engine(DB_URI, echo=True)
Session = sessionmaker(bind=engine)

class Fulfillment(Base):
    __tablename__ = 'fulfillment'
    fulfillment_id = Column(String(36), primary_key=True)
    order_id = Column(String(36), primary_key=True)
    status = Column(String(36))

def create_fulfillment_object(order):
    if order["status"] == "MERCHANT_ACCEPTED":
        fulfillmentStatus = "SHIPPED"
    else:
        fulfillmentStatus = "DELIVERED"

    return {
        "order_id": order.get("order_id"),
        "fulfillment_id": str(uuid.uuid4()),
        "status": fulfillmentStatus,
    }

input_path = "data/logs.txt"
output_path = "data/filtered_logs.txt"

if __name__ == "__main__":
    with open(input_path, "r") as infile, open(output_path, "w") as outfile:
        for line in infile:
            if " 200 " in line:
                outfile.write(line)
    print(f"Gefilterte Logzeilen nach {output_path} geschrieben.")


DB_URI = 'mysql+pymysql://user:userpw@[fd00:dead:cafe::100]:3306/fulfillment'
engine = create_engine(DB_URI, echo=True)
Session = sessionmaker(bind=engine)


# === Kafka Consumer ===
kafka_conf_merchant_accepted = {
    'bootstrap.servers': '[fd00:dead:cafe::10]:9092',
    'group.id': 'fulfillment-processing-group',
    'auto.offset.reset': 'earliest'
}


consumer = Consumer(kafka_conf_merchant_accepted)
consumer.subscribe(['order'])
print("? Warte auf Order-Events ...")

conf = {
    'bootstrap.servers': '[fd00:dead:cafe::10]:9092',
    'client.id': 'fulfillment-producer'
}

producer = Producer(conf)

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())

        session = Session()

        try:
            payload = json.loads(msg.value().decode('utf-8'))

            if payload.get("status") != "MERCHANT_ACCEPTED" and payload.get("status") != "SHIPPED":
                print("? Wrong Order Status received - do not process: "+ payload.get('status'))

            if payload.get("status") == "MERCHANT_ACCEPTED":
                # create fulfillment_object
                fulfillment_object = create_fulfillment_object(payload)

                # save in db
                session.add(fulfillment_object)
                session.commit()

                # produce into db
                producer.produce(
                    topic="fulfillment",
                    key=fulfillment_object["fulfillment_id"],
                    value=json.dumps(fulfillment_object),
                    callback=delivery_report
                )
                print("? Received MERCHANT_ACCEPTED - SHIPPED")

            if payload.get("status") == "SHIPPED":
                producer.produce(
                    topic="fulfillment",
                    key=fulfillment_object["fulfillment_id"],
                    value=json.dumps(fulfillment_object),
                    callback=delivery_report
                )

                print("? RECEIVED SHIPPED - DELIVERED")
except:
    print("? Aborted through User")
finally:
    consumer.close()