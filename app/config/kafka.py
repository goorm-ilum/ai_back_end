from kafka import KafkaConsumer, KafkaProducer
import json

KAFKA_BROKER = "172.16.24.72:9092"

# Consumer 설정
consumer = KafkaConsumer(
    'review.raw',
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='earliest',
    group_id='fastapi-ai-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)
