from fastapi import FastAPI, Depends
from database.conn import connection_db, close_db
from contextlib import asynccontextmanager
from routes import all_routers
from database.indexes import create_indexes
import os

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connection_db(app)
    db = app.state.db
    await create_indexes(db)
    yield
    await close_db(app)


app = FastAPI(lifespan=lifespan)

for router in all_routers:
    app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}