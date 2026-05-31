from motor.motor_asyncio import AsyncIOMotorDatabase

async def create_indexes(db: AsyncIOMotorDatabase):
    await db.features.create_index("name", unique=True)