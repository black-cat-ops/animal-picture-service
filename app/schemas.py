from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AnimalPictureRequest(BaseModel):
    animal_type: str = Field(..., description="Type of animal: cat, dog, or bear")
    width: int = Field(default=400, description="Image width")
    height: int = Field(default=400, description="Image height")

class AnimalPictureResponse(BaseModel):
    id: int
    animal_type: str
    image_url: str
    width: int
    height: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class HealthResponse(BaseModel):
    status: str
    version: str
    database: str
