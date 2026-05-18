from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from database.depn import get_db
from feature_schema import createFeatureSchema, FeatureResponse
from datetime import datetime

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
    existing_feature = await db.features.find_one({"name": payload.name})
    if existing_feature:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Feature already exists")

    now = datetime.now()
    doc = {**payload.model_dump(), "created_at": now, "updated_at": now}
    feature = await db.features.insert_one(doc)
    print(feature)
    print('feature.inserted_id', feature.inserted_id)
    created_feature = await db.features.find_one({"_id": feature.inserted_id})
    print('created_feature', created_feature)
    return FeatureResponse.model_validate(created_feature)