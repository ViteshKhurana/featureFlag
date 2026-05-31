from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

class createFeatureSchema(BaseModel):
    name: str=Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    is_enabled: bool=False
    rollout_percentage: int=Field(
        default=0,
        ge=0,
        le=100
    )

class updateFeatureSchema(BaseModel):
    description: Optional[str] = None
    is_enabled: Optional[bool] = None
    rollout_percentage: Optional[int] = Field(
        default=None,
        ge=0,
        le=100
    )

class FeatureResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(validation_alias="_id")
    name: str
    description: Optional[str] = None
    is_enabled: bool
    rollout_percentage: int
    created_at: datetime
    updated_at: datetime

    @field_validator("id", mode="before")
    @classmethod
    def id_to_str(cls, v: Any) -> str:
        return str(v)