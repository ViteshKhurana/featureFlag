from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from schemas.feature_schema import createFeatureSchema, FeatureResponse, updateFeatureSchema
from repositories.feature_repo import (
    create_feature_repo,
    get_feature_by_name_repo,
    get_feature_repo,
    update_feature_repo,
    delete_feature_repo,
)

async def create_feature_service(db: AsyncIOMotorClient, payload: createFeatureSchema):
    existing_feature = await get_feature_by_name_repo(db, payload.name)
    if existing_feature:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Feature already exists")

    feature_id = await create_feature_repo(db, payload)
    print('feature_id', feature_id, type(feature_id))
    created_feature = await get_feature_repo(db, feature_id)
    print('created_feature', created_feature)
    return FeatureResponse.model_validate(created_feature)

async def update_feature_service(db: AsyncIOMotorClient, feature_id: str, payload: updateFeatureSchema):
    existing_feature = await get_feature_repo(db, feature_id)
    if not existing_feature:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feature not found")

    update_feature = await update_feature_repo(db, feature_id, payload)

    updated_feature = await get_feature_repo(db, feature_id);
    return FeatureResponse.model_validate(updated_feature)

async def delete_feature_service(db: AsyncIOMotorClient, feature_id: str):
    existing_feature = await get_feature_repo(db, feature_id)
    if not existing_feature:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feature not found")

    return await delete_feature_repo(db, feature_id)
     


