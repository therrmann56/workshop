# filter/main.py
# Dieses Skript liest Logzeilen ein und filtert nur Zeilen mit dem Statuscode 200.

import json
import uuid
from datetime import datetime
from confluent_kafka import Consumer, KafkaException
from sqlalchemy import create_engine, Column, String, Integer, DECIMAL, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

input_path = "data/logs.txt"
output_path = "data/filtered_logs.txt"

if __name__ == "__main__":
    with open(input_path, "r") as infile, open(output_path, "w") as outfile:
        for line in infile:
            if " 200 " in line:
                outfile.write(line)
    print(f"Gefilterte Logzeilen nach {output_path} geschrieben.")


DB_URI = 'mysql+pymysql://user:userpw@[fd00:dead:cafe::100]:3306/analytics'
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

try:
    while true:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())

        session = Session()

        try:
            payload = json.loads(msg.value().decode('utf-8'))
            if payload.get("status") == "MERCHANT_ACCEPTED":
                # FULFILLMENT
            elif payload.get("status") == "SHIPPED":
                # Completed


except:

finally: