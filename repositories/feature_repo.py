from datetime import datetime, UTC
from typing import Union

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from schemas.feature_schema import CreateFeatureSchema, UpdateFeatureSchema


def _to_object_id(feature_id: Union[str, ObjectId]) -> ObjectId:
    if isinstance(feature_id, ObjectId):
        return feature_id
    return ObjectId(feature_id)


async def create_feature_repo(db: AsyncIOMotorDatabase, payload: createFeatureSchema):
    now = datetime.now(UTC)
    doc = {**payload.model_dump(), "created_at": now, "updated_at": now}
    feature = await db.features.insert_one(doc)
    return feature.inserted_id


async def get_feature_by_name_repo(db: AsyncIOMotorDatabase, name: str):
    return await db.features.find_one({"name": name})


async def get_feature_repo(db: AsyncIOMotorDatabase, feature_id: Union[str, ObjectId]):
    return await db.features.find_one({"_id": _to_object_id(feature_id)})


async def update_feature_repo(
    db: AsyncIOMotorDatabase, feature_id: str, payload: UpdateFeatureSchema
):
    now = datetime.now(UTC)
    return await db.features.update_one(
        {"_id": _to_object_id(feature_id)},
        {"$set": {**payload.model_dump(exclude_unset=True), "updated_at": now}},
    )

async def delete_feature_repo(db: AsyncIOMotorDatabase, feature_id: str):
    return await db.features.delete_one({"_id": _to_object_id(feature_id)})