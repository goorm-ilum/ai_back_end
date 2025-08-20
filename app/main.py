import threading
from fastapi import FastAPI
from app.routes.products import router

app = FastAPI()
app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "AI SQL Agent API"}

def consume_kafka():
    try:
        from app.config.kafka import consumer
        for message in consumer:
            data = message.value
            print(f"[Kafka] 받은 메시지: {data}")
    except Exception as e:
        print(f"[Kafka] Consumer 연결 실패: {e}")

# 백그라운드 스레드에서 안전하게 실행
threading.Thread(target=consume_kafka, daemon=True).start()
