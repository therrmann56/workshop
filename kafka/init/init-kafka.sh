#!/bin/sh

BOOTSTRAP_SERVER="kafka:9092"
TOPICS="order fulfillment checkout"

echo "⏳ Waiting for Kafka to become available at $BOOTSTRAP_SERVER..."
MAX_WAIT=60
COUNT=0

until kafka-topics --bootstrap-server "$BOOTSTRAP_SERVER" --list >/dev/null 2>&1; do
  if [ $COUNT -ge $MAX_WAIT ]; then
    echo "❌ Kafka not available after $MAX_WAIT seconds, exiting."
    exit 1
  fi
  COUNT=$((COUNT + 1))
  echo "Waiting... ($COUNT)"
  sleep 1
done

echo "✅ Kafka is available. Creating topics..."

for topic in $TOPICS; do
  echo "➡ Creating topic: $topic"
  kafka-topics --bootstrap-server "$BOOTSTRAP_SERVER" \
    --create --if-not-exists \
    --topic "$topic" --partitions 1 --replication-factor 1
done

echo "🏁 All topics created."
