import threading
from fastapi import FastAPI
from app.routes.products import router
from app.config.kafka import consumer, producer
from app.services.ai_model import run_inference

app = FastAPI()
app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "AI SQL Agent API"}

def consume_kafka():
    for message in consumer:
        data = message.value
        result = run_inference(data)
        producer.send("review.processed", result)
        producer.flush()

# 백그라운드 스레드로 실행 / daemon=True로 설정하여 메인 스레드 종료 시 자동 종료
threading.Thread(target=consume_kafka, daemon=True).start()
