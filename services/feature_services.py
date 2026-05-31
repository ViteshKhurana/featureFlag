from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from schemas.feature_schema import CreateFeatureSchema, FeatureResponse, UpdateFeatureSchema, GetFeaturesResponse
from repositories.feature_repo import (
    create_feature_repo,
    get_feature_by_name_repo,
    get_feature_repo,
    update_feature_repo,
    delete_feature_repo,
)
from bson import ObjectId
from bson.errors import InvalidId

async def get_features_service(db: AsyncIOMotorDatabase, offset: int, limit: int):
    docs = await db.features.find().skip(offset).limit(limit).to_list()
    total = await db.features.count_documents({})
    return GetFeaturesResponse(features=[FeatureResponse.model_validate(doc) for doc in docs], 
    total=total, page=offset, limit=limit)

async def create_feature_service(db: AsyncIOMotorDatabase, payload: CreateFeatureSchema):
    existing_feature = await get_feature_by_name_repo(db, payload.name)
    if existing_feature:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Feature already exists")

    feature_id = await create_feature_repo(db, payload)
    created_feature = await get_feature_repo(db, feature_id)
    return FeatureResponse.model_validate(created_feature)

async def update_feature_service(db: AsyncIOMotorDatabase, feature_id: str, payload: UpdateFeatureSchema):
    try:
        is_valid_id = ObjectId(feature_id)
        if not payload.model_dump(exclude_unset=True):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")
        existing_feature = await get_feature_repo(db, feature_id)
        if not existing_feature:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feature not found")

        update_feature = await update_feature_repo(db, feature_id, payload)

        updated_feature = await get_feature_repo(db, feature_id);
        return FeatureResponse.model_validate(updated_feature)
    except InvalidId as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid feature ID')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def delete_feature_service(db: AsyncIOMotorDatabase, feature_id: str):
    try:
        is_valid_id = ObjectId(feature_id)
        existing_feature = await get_feature_repo(db, feature_id)
        if not existing_feature:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feature not found")

        return await delete_feature_repo(db, feature_id)
    except InvalidId as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid feature ID')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


