from aiokafka import AIOKafkaConsumer
import json

KAFKA_BROKER = "172.16.24.72:9092"

# Consumer 설정
consumer = AIOKafkaConsumer(
    'review.raw',
    bootstrap_servers="172.16.24.72:9092",
    group_id="fastapi-ai-group",
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)
