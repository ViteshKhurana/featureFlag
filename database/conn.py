from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")

client = AsyncIOMotorClient(mongo_uri)
db = client[db_name]

async def get_database():
    return db