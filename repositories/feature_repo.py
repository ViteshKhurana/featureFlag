from datetime import datetime
from typing import Union

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from schemas.feature_schema import createFeatureSchema, updateFeatureSchema


def _to_object_id(feature_id: Union[str, ObjectId]) -> ObjectId:
    if isinstance(feature_id, ObjectId):
        return feature_id
    return ObjectId(feature_id)


async def create_feature_repo(db: AsyncIOMotorClient, payload: createFeatureSchema):
    now = datetime.now()
    doc = {**payload.model_dump(), "created_at": now, "updated_at": now}
    feature = await db.features.insert_one(doc)
    return feature.inserted_id


async def get_feature_by_name_repo(db: AsyncIOMotorClient, name: str):
    return await db.features.find_one({"name": name})


async def get_feature_repo(db: AsyncIOMotorClient, feature_id: Union[str, ObjectId]):
    return await db.features.find_one({"_id": _to_object_id(feature_id)})


async def update_feature_repo(
    db: AsyncIOMotorClient, feature_id: str, payload: updateFeatureSchema
):
    now = datetime.now()
    return await db.features.update_one(
        {"_id": _to_object_id(feature_id)},
        {"$set": {**payload.model_dump(exclude_unset=True), "updated_at": now}},
    )

async def delete_feature_repo(db: AsyncIOMotorClient, feature_id: str):
    return await db.features.delete_one({"_id": _to_object_id(feature_id)})