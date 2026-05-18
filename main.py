from fastapi import FastAPI
from database.conn import connection_db, close_db
from contextlib import asynccontextmanager
from routes import all_routers
import os

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connection_db(app)
    yield
    await close_db(app)


app = FastAPI(lifespan=lifespan)

for router in all_routers:
    app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}