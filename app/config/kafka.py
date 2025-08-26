from aiokafka import AIOKafkaConsumer
import json
from pydantic_settings import BaseSettings

class KafkaSettings(BaseSettings):
    bootstrap_servers: str = "localhost:9092,localhost:9093,localhost:9094"
    topic: str = "review.raw"
    group_id: str = "review-consumer-group"
    
    class Config:
        env_prefix = "KAFKA_"  # 환경변수 앞에 KAFKA_ 붙여서 읽기

# 설정 인스턴스 생성
kafka_config = KafkaSettings()

# 브로커 리스트로 변환
KAFKA_BROKERS = kafka_config.bootstrap_servers.split(",")

# Consumer 설정
consumer = AIOKafkaConsumer(
    kafka_config.topic,
    bootstrap_servers=KAFKA_BROKERS,
    group_id=kafka_config.group_id,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)