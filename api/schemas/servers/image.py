from pydantic import BaseModel, Field
from typing import List



class ServerImageSchema(BaseModel):
    id: int | None = None
    name: str = Field(..., description="The name of the server image")
    version: str = Field(..., description="The version of the server image")
    source: str = Field(..., description="The source of the server image")
    logo: str = Field(..., description="The logo of the server image")
    available: bool = Field(..., description="Whether the server image is available")
    service_id: int = Field(..., description="The ID of the service")
    regions: List[int] = Field(default=[], description="List of region IDs where this image is available")


class ServerImageCreateSchema(BaseModel):
    name: str = Field(..., description="The name of the server image")
    version: str = Field(..., description="The version of the server image")
    source: str = Field(..., description="The source of the server image")
    logo: str = Field(..., description="The logo of the server image")
    available: bool = Field(..., description="Whether the server image is available")
    service_id: int = Field(..., description="The ID of the service")
    regions: List[int] = Field(default=[], description="List of region IDs where this image is available")


class ServerImageUpdateSchema(BaseModel):
    name: str | None = Field(default=None, description="The name of the server image")
    version: str | None = Field(default=None, description="The version of the server image")
    source: str | None = Field(default=None, description="The source of the server image")
    logo: str | None = Field(default=None, description="The logo of the server image")
    available: bool | None = Field(default=None, description="Whether the server image is available")
    service_id: int | None = Field(default=None, description="The ID of the service")
