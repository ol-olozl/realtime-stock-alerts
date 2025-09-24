import os, json, random, time
from datetime import datetime, timezone, timedelta
from kafka import KafkaProducer

broker = os.getenv("KAFKA_BROKER","localhost:29092")
topic = os.getenv("KAFKA_TOPIC_PRICES","stock_prices")
symbols = os.getenv("SYMBOLS","005930,NVDA,AVGO").split(",")

producer = KafkaProducer(
    bootstrap_servers=broker,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8"),
)

print(f"[load_test] sending ticks to {broker}/{topic} for {symbols}")

base = {s: 100.0 + random.random()*5 for s in symbols}
tz = timezone(timedelta(hours=9))

try:
    while True:
        for s in symbols:
            # random walk
            base[s] += random.uniform(-0.5, 0.5)
            msg = {
                "ts": datetime.now(tz).isoformat(),
                "symbol": s,
                "price": round(base[s], 2),
                "source": "mock"
            }
            producer.send(topic, key=s, value=msg)
        producer.flush()
        time.sleep(float(os.getenv("PRICE_POLL_INTERVAL_SEC","2")))
except KeyboardInterrupt:
    print("\n[load_test] stopped")
