CREATE DATABASE IF NOT EXISTS markets;

CREATE TABLE IF NOT EXISTS markets.ticks (
  ts DateTime64(3, 'Asia/Seoul'),
  ts_ttl DateTime('Asia/Seoul') MATERIALIZED toDateTime(ts),
  symbol LowCardinality(String),
  price Float64,
  source LowCardinality(String)
) ENGINE = MergeTree
ORDER BY (symbol, ts)
TTL ts_ttl + INTERVAL 7 DAY;

CREATE TABLE IF NOT EXISTS markets.metrics (
  ts DateTime64(3, 'Asia/Seoul'),
  symbol LowCardinality(String),
  price Float64,
  pct_change_5m Float64,
  pct_change_15m Float64
) ENGINE = MergeTree
ORDER BY (symbol, ts);

CREATE TABLE IF NOT EXISTS markets.alerts (
  ts DateTime64(3, 'Asia/Seoul'),
  symbol LowCardinality(String),
  price Float64,
  direction Int8,
  threshold_pct Float64,
  window String,
  rule_id String,
  message String
) ENGINE = MergeTree
ORDER BY (ts, symbol);
