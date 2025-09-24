import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from clickhouse_driver import Client
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9)) # Asia/Seoul 타임존
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC = os.getenv("KAFKA_TOPIC_PRICES", "stock_prices")

CH_HOST = os.getenv("CH_HOST", "clickhouse")
CH_PORT = int(os.getenv("CH_PORT", "9000"))
CH_USER = os.getenv("CH_USER", "default")
CH_PASSWORD = os.getenv("CH_PASSWORD", "")
CH_DB = os.getenv("CH_DB", "markets")

schema = StructType([
    StructField("ts", StringType(), True),
    StructField("symbol", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("source", StringType(), True),
])

def to_datetime(ts: str):
    if ts is None:
        return None
    s = ts.replace('Z', '+00:00')
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        s2 = s.replace('T', ' ')
        try:
            dt = datetime.fromisoformat(s2)
        except Exception:
            return None

    if dt.tzinfo is not None:
        dt = dt.astimezone(KST).replace(tzinfo=None)
    return dt

def write_ticks_to_clickhouse(df, _):
    rows = df.select("ts", "symbol", "price", "source").toLocalIterator()

    client = Client(host=CH_HOST, port=CH_PORT, user=CH_USER,
                    password=CH_PASSWORD, database=CH_DB)
    batch = []
    for r in rows:
        batch.append((
            to_datetime(r["ts"]),
            r["symbol"],
            float(r["price"]) if r["price"] is not None else None,
            r["source"],
        ))
        if len(batch) >= 5000:
            client.execute(
                "INSERT INTO markets.ticks (ts, symbol, price, source) VALUES",
                batch
            )
            batch.clear()
    if batch:
        client.execute(
            "INSERT INTO markets.ticks (ts, symbol, price, source) VALUES",
            batch
        )

if __name__ == "__main__":
    spark = (SparkSession.builder.appName("stock-ticks-to-clickhouse").getOrCreate())
    spark.sparkContext.setLogLevel("WARN")

    raw = (spark.readStream
           .format("kafka")
           .option("kafka.bootstrap.servers", KAFKA_BROKER)
           .option("subscribe", TOPIC)
           .option("startingOffsets", "latest")
           .load())

    parsed = (raw.select(from_json(col("value").cast("string"), schema).alias("j"))
                   .select("j.*")
                   .dropna(subset=["symbol","price"]))

    query = (parsed.writeStream
             .foreachBatch(write_ticks_to_clickhouse)
             .option("checkpointLocation", "/tmp/chk_stock_ticks")
             .start())

    query.awaitTermination()
