# Realtime Stock Alerts 

### Goal
Demonstrate real-time data pipeline design and event-driven alerting as a portfolio project.

### Architecture
FastAPI → Kafka → Spark → ClickHouse → Email Alerts

### Components
- FastAPI: Pulls stock prices from external APIs, exposes REST endpoints for alert rules, and sends alert emails.
- Kafka: Serves as a message broker and buffer between services.
- Spark: Performs real-time percentage change analysis and applies alert conditions.
- ClickHouse: Stores raw ticks, metrics, and alerts for ultra-low-latency queries.

### Why this project?
This project is a full-stack real-time stock monitoring system designed to demonstrate how event-driven pipelines can enable faster and more convenient decision-making in trading.

- Instead of waiting for delayed batch reports, traders can receive instant alerts (e.g., price up/down ±5%) directly in their inbox.
- Storing both raw ticks and derived metrics allows deep analysis and flexible dashboards with near-zero latency.
- The system showcases modern data engineering skills: streaming ingestion, distributed processing, alerting, and visualization — all in a containerized environment.
