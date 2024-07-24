from pydantic import BaseModel, Field
from typing import Optional


class ServiceFilterParams(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    available: Optional[bool] = None


class ServiceSchema(BaseModel):
    id: int | None = None
    name: str = Field(..., description="The name of the service")
    description: str = Field(..., description="The description of the service")
    available: bool = Field(..., description="The availability of the service")


class ServiceCreateSchema(BaseModel):
    name: str = Field(..., description="The name of the service")
    description: str = Field(..., description="The description of the service")
    available: bool = Field(..., description="The availability of the service")


class ServiceUpdateSchema(BaseModel):
    name: str | None = Field(default=None, description="The name of the service")
    description: str | None = Field(default=None, description="The description of the service")
    available: bool | None = Field(default=None, description="The availability of the service")
