from pydantic import BaseModel, Field
from typing import Optional


class RegionFilterParams(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    available: Optional[bool] = None


class RegionSchema(BaseModel):
    id: int | None = None
    name: str = Field(..., description="The name of the region")
    logo: str = Field(..., description="The URL logo of the region")
    available: bool = Field(..., description="The availability of the region")


class RegionCreateSchema(BaseModel):
    name: str = Field(..., description="The name of the region")
    logo: str = Field(..., description="The URL logo of the region")
    available: bool = Field(..., description="The availability of the region")


class RegionUpdateSchema(BaseModel):
    name: str | None = Field(default=None, description="The name of the region")
    logo: str | None = Field(default=None, description="The URL logo of the region")
    available: bool | None = Field(default=None, description="The availability of the region")
