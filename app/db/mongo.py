from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import MONGODB_URL

mongo_client: AsyncIOMotorClient = None
mongo_db = None
review_keywords_collection = None

async def connect_to_mongo():
    mongo_client = AsyncIOMotorClient(MONGODB_URL)
    mongo_db = mongo_client["TalkTrip"]
    review_keywords_collection = mongo_db["review_keywords"]
    print("[MongoDB] 연결 완료:", review_keywords_collection)
    return review_keywords_collection

async def close_mongo_connection():
    global mongo_client
    if mongo_client is not None:
        mongo_client.close()

def get_mongo_db():
    return mongo_db
