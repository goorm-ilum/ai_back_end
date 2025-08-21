from fastapi import FastAPI
from app.routes.products import router
from app.config.kafka import consumer
from app.services.ai_model import run_inference
from app.db.mongo import connect_to_mongo, close_mongo_connection, review_keywords_collection
import asyncio

app = FastAPI()
app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "AI SQL Agent API"}

async def consume_kafka():
    while review_keywords_collection is None:
        print("[MongoDB] 컬렉션 준비 대기 중...")
        await asyncio.sleep(0.5)

    try:
        await consumer.start()
        async for message in consumer:
            data = message.value
            print(f"[Kafka] 받은 메시지: {data}")

            results =await asyncio.to_thread(run_inference, data)
            print(f"[Inference] 결과: {results}")

            if results and review_keywords_collection is not None:
                await review_keywords_collection.insert_many(results)
                print(f"[MongoDB] {len(results)}개 결과 저장 완료")
    except Exception as e:
        print(f"[Kafka] Consumer 연결 실패: {e}")
    finally:
        await consumer.stop()

@app.on_event("startup")
async def startup_db_client():
    global review_keywords_collection
    review_keywords_collection = await connect_to_mongo()
    print(f"[MongoDB] 컬렉션 확인: {review_keywords_collection}")
    asyncio.create_task(consume_kafka())

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()
