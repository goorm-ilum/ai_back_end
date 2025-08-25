from aiokafka import AIOKafkaConsumer
import json

KAFKA_BROKERS = [
    "172.16.24.72:19092",
    "172.16.24.72:29092",
    "172.16.24.72:39092"
]

# Consumer 설정
consumer = AIOKafkaConsumer(
    'review.raw',
    bootstrap_servers=KAFKA_BROKERS,
    group_id="fastapi-ai-group",
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)
