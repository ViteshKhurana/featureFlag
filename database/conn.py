from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")

async def connection_db(app: FastAPI):
    client = AsyncIOMotorClient(mongo_uri)
    app.state.mongo_client = client
    app.state.db = client[db_name]

async def close_db(app: FastAPI):
    app.state.mongo_client.close()