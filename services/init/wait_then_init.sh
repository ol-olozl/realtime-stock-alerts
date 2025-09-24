#!/usr/bin/env bash
set -euo pipefail

# 서비스 기동 대기
sleep 8 || true

# 토픽 생성
/init/create_topics.sh || true

# ClickHouse 스키마 적용
clickhouse-client --host "${CH_HOST:-clickhouse}" --port "${CH_PORT:-8123}" \
  --user "${CH_USER:-default}" --password "${CH_PASSWORD:-}" \
  --queries-file /init/clickhouse_schemas.sql || true

echo "[init] topics & schemas ready."
