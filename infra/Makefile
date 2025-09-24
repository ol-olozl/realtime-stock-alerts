include .env

.PHONY: up down logs topics migrate seed ch-sql

up:
	docker compose -f infra/docker-compose.yml up -d --build

logs:
	docker compose -f infra/docker-compose.yml logs -f --tail=200

down:
	docker compose -f infra/docker-compose.yml down -v

ch-sql:
	@docker compose -f infra/docker-compose.yml exec -T clickhouse \
	  bash -lc "clickhouse-client --query='$$SQL'"

topics:
	@docker compose -f infra/docker-compose.yml exec -T kafka bash -lc "/opt/bitnami/kafka/bin/kafka-topics.sh --bootstrap-server kafka:9092 --create --if-not-exists --topic stock_prices --partitions 3 --replication-factor 1"
	@docker compose -f infra/docker-compose.yml exec -T kafka bash -lc "/opt/bitnami/kafka/bin/kafka-topics.sh --bootstrap-server kafka:9092 --create --if-not-exists --topic alerts --partitions 1 --replication-factor 1"
	@docker compose -f infra/docker-compose.yml exec -T kafka bash -lc "/opt/bitnami/kafka/bin/kafka-topics.sh --bootstrap-server kafka:9092 --list"

migrate:
	@docker compose -f infra/docker-compose.yml exec -T clickhouse bash -lc "clickhouse-client --host $$CH_HOST --port $$CH_PORT --user $$CH_USER --password $$CH_PASSWORD --queries-file /init/clickhouse_schemas.sql"

seed:
	python3 scripts/load_test.py
