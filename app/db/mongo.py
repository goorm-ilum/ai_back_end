from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import MONGODB_URL

mongo_client = AsyncIOMotorClient(MONGODB_URL)
mongo_db = mongo_client["TalkTrip"]

def get_mongo_db():
    return mongo_db
