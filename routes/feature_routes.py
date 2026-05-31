from fastapi import APIRouter, Depends, status
from motor.motor_asyncio import AsyncIOMotorClient
from database.depn import get_db
from schemas.feature_schema import createFeatureSchema, FeatureResponse, updateFeatureSchema
from services.feature_services import create_feature_service, update_feature_service, delete_feature_service

router = APIRouter(
    prefix="/features",
    tags=["Features"]
)

@router.get("/", response_model=list[FeatureResponse])
async def get_features(db: AsyncIOMotorClient = Depends(get_db)):
    docs = await db.features.find().to_list()
    return [FeatureResponse.model_validate(doc) for doc in docs]

@router.post("/", response_model=FeatureResponse, status_code=status.HTTP_201_CREATED)
async def create_feature(payload: createFeatureSchema, db: AsyncIOMotorClient = Depends(get_db)):
    return await create_feature_service(db, payload)

@router.patch("/{feature_id}", response_model=FeatureResponse, status_code=status.HTTP_200_OK)
async def update_feature(feature_id: str, payload: updateFeatureSchema, db: AsyncIOMotorClient = Depends(get_db)):
    return await update_feature_service(db, feature_id, payload)

@router.delete("/{feature_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_feature(feature_id: str, db: AsyncIOMotorClient = Depends(get_db)):
    await delete_feature_service(db, feature_id)