from fastapi import APIRouter, Depends, status, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from database.depn import get_db
from schemas.feature_schema import CreateFeatureSchema, FeatureResponse, UpdateFeatureSchema, GetFeaturesResponse, GetFeaturesParams
from services.feature_services import create_feature_service, update_feature_service, delete_feature_service, get_features_service

router = APIRouter(
    prefix="/features",
    tags=["Features"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=GetFeaturesResponse)
async def get_features(
    db: AsyncIOMotorDatabase = Depends(get_db),
    params: GetFeaturesParams = Depends()
):
    offset = params.offset
    limit = params.limit
    return await get_features_service(db, offset, limit)

@router.post("/", response_model=FeatureResponse, status_code=status.HTTP_201_CREATED)
async def create_feature(payload: CreateFeatureSchema, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await create_feature_service(db, payload)

@router.patch("/{feature_id}", response_model=FeatureResponse, status_code=status.HTTP_200_OK)
async def update_feature(feature_id: str, payload: UpdateFeatureSchema, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await update_feature_service(db, feature_id, payload)

@router.delete("/{feature_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_feature(feature_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    await delete_feature_service(db, feature_id)