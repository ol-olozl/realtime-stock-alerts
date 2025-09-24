#!/usr/bin/env bash
set -euo pipefail

BROKER="${KAFKA_BROKER:-kafka:9092}"

"/opt/bitnami/kafka/bin/kafka-topics.sh" --bootstrap-server "$BROKER" \
  --create --if-not-exists --topic stock_prices --partitions 3 --replication-factor 1

"/opt/bitnami/kafka/bin/kafka-topics.sh" --bootstrap-server "$BROKER" \
  --create --if-not-exists --topic alerts --partitions 1 --replication-factor 1

"/opt/bitnami/kafka/bin/kafka-topics.sh" --bootstrap-server "$BROKER" --list
