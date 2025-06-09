# -*- coding: utf-8 -*-

# simples skript, dass checkouts konsumiert, wenn der Status "CheckoutSubmitted" gesetzt ist und als Order in der DB speichert. Alles andere muss implementiert werden.

import json
import uuid
from datetime import datetime
from confluent_kafka import Consumer, KafkaException
from sqlalchemy import create_engine, Column, String, Integer, DECIMAL, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()

# Datenbankverbindung
DB_URI = 'mysql+pymysql://user:userpw@[fd00:dead:cafe::100]:3306/analytics'
engine = create_engine(DB_URI, echo=True)
Session = sessionmaker(bind=engine)

# === ORM-Modelle ===
class Order(Base):
    __tablename__ = 'order'
    order_id = Column(String(36), primary_key=True)
    checkout_id = Column(String(36), unique=True, nullable=False)
    user_id = Column(String(36))
    total_amount = Column(DECIMAL(10, 2))
    currency = Column(String(3))
    payment_method = Column(String(50))
    status = Column(String(20))
    created_at = Column(DateTime)

    shipping_address = relationship("OrderShippingAddress", back_populates="order", uselist=False, cascade="all, delete-orphan")
    cart_items = relationship("OrderCartItem", back_populates="order", cascade="all, delete-orphan")

class OrderShippingAddress(Base):
    __tablename__ = 'order_shipping_address'
    checkout_id = Column(String(36), ForeignKey('order.checkout_id'), primary_key=True)
    name = Column(String(100))
    street = Column(String(100))
    zip = Column(String(10))
    city = Column(String(50))
    country = Column(String(5))

    order = relationship("Order", back_populates="shipping_address")

class OrderCartItem(Base):
    __tablename__ = 'order_cart_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    checkout_id = Column(String(36), ForeignKey('order.checkout_id'))
    product_id = Column(String(50))
    quantity = Column(Integer)
    price = Column(DECIMAL(10, 2))

    order = relationship("Order", back_populates="cart_items")


# === Kafka Consumer ===
kafka_conf = {
    'bootstrap.servers': '[fd00:dead:cafe::10]:9092',
    'group.id': 'order-processor-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(kafka_conf)
consumer.subscribe(['checkout'])

print("? Warte auf Checkout-Events ...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())

        try:
            payload = json.loads(msg.value().decode('utf-8'))
            if payload.get("status") != "CheckoutSubmitted":
                continue

            order = Order(
                order_id=str(uuid.uuid4()),
                checkout_id=payload["checkout_id"],
                user_id=payload["user_id"],
                total_amount=payload["total_amount"],
                currency=payload["currency"],
                payment_method=payload["payment_method"],
                status="NEW",
                created_at=datetime.fromisoformat(payload["created_at"].replace("Z", ""))
            )

            address = payload.get("shipping_address", {})
            order.shipping_address = OrderShippingAddress(
                checkout_id=order.checkout_id,
                name=address.get("name"),
                street=address.get("street"),
                zip=address.get("zip"),
                city=address.get("city"),
                country=address.get("country")
            )

            order.cart_items = [
                OrderCartItem(
                    checkout_id=order.checkout_id,
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    price=item["price"]
                ) for item in payload.get("cart_items", [])
            ]

            session = Session()
            session.add(order)
            session.commit()
            print(f"? Order {order.order_id} gespeichert.")

        except SQLAlchemyError as db_err:
            print("? DB-Fehler:", db_err)
            session.rollback()
        except Exception as parse_err:
            print("? Verarbeitungsfehler:", parse_err)
        finally:
            session.close()

except KeyboardInterrupt:
    print("? Verarbeitung abgebrochen durch Benutzer.")
finally:
    consumer.close()
