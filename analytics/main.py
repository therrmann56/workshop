# -*- coding: utf-8 -*-
from datetime import datetime
import json
import uuid
from confluent_kafka import Consumer, KafkaException
from sqlalchemy import create_engine, Column, String, Integer, DECIMAL, DateTime, ForeignKey, text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()

# ORM-Modelle (wie zuvor)
class Checkout(Base):
    __tablename__ = 'checkout'
    checkout_id = Column(String(36), primary_key=True)
    user_id = Column(String(36))
    total_amount = Column(DECIMAL(10, 2))
    currency = Column(String(3))
    payment_method = Column(String(50))
    status = Column(String(20))
    created_at = Column(DateTime)

    shipping_address = relationship("ShippingAddress", back_populates="checkout", uselist=False, cascade="all, delete-orphan")
    cart_items = relationship("CartItem", back_populates="checkout", cascade="all, delete-orphan")


class ShippingAddress(Base):
    __tablename__ = 'shipping_address'
    checkout_id = Column(String(36), ForeignKey('checkout.checkout_id'), primary_key=True)
    name = Column(String(100))
    street = Column(String(100))
    zip = Column(String(10))
    city = Column(String(50))
    country = Column(String(5))
    checkout = relationship("Checkout", back_populates="shipping_address")


class CartItem(Base):
    __tablename__ = 'cart_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    checkout_id = Column(String(36), ForeignKey('checkout.checkout_id'))
    product_id = Column(String(50))
    quantity = Column(Integer)
    price = Column(DECIMAL(10, 2))
    checkout = relationship("Checkout", back_populates="cart_items")


# DB-Verbindung über IPv6 oder Containername
DB_URI = 'mysql+pymysql://user:userpw@[fd00:dead:cafe::100]:3306/analytics'
engine = create_engine(DB_URI, echo=True)
Session = sessionmaker(bind=engine)

# Kafka-Consumer-Konfiguration
conf = {
    'bootstrap.servers': '[fd00:dead:cafe::10]:9092',
    'group.id': 'analytics-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['checkout'])

print("✅ Warte auf Kafka-Nachrichten im Topic 'checkout'...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())

        payload = json.loads(msg.value().decode('utf-8'))
        print(f"📦 Empfangen: {payload}")

        session = Session()
        try:
            checkout_id = payload.get("checkout_id", str(uuid.uuid4()))
            new_checkout = Checkout(
                checkout_id=checkout_id,
                user_id=payload["user_id"],
                total_amount=payload["total_amount"],
                currency=payload["currency"],
                payment_method=payload["payment_method"],
                status=payload["status"],
                created_at=datetime.fromisoformat(payload["created_at"].replace("Z", "+00:00"))
            )

            new_checkout.shipping_address = ShippingAddress(
                checkout_id=checkout_id,
                name=payload["shipping_address"]["name"],
                street=payload["shipping_address"]["street"],
                zip=payload["shipping_address"]["zip"],
                city=payload["shipping_address"]["city"],
                country=payload["shipping_address"]["country"]
            )

            new_checkout.cart_items = [
                CartItem(
                    checkout_id=checkout_id,
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    price=item["price"]
                ) for item in payload["cart_items"]
            ]

            session.add(new_checkout)
            session.commit()
            print(f"✅ Checkout gespeichert: {checkout_id}")
        except SQLAlchemyError as e:
            print(f"❌ Datenbankfehler: {e}")
            session.rollback()
        finally:
            session.close()

except KeyboardInterrupt:
    print("⛔ Abbruch durch Benutzer")
finally:
    consumer.close()
