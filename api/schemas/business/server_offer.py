from pydantic import BaseModel, Field


class ServerOfferSchema(BaseModel):
    id: int | None = None
    price: float = Field(..., description="The price of the server offer")
    currency: str = Field(..., description="The currency of the server offer")
    cpu: int = Field(..., description="The number of CPU cores")
    memory: int = Field(..., description="The amount of memory in MB")
    storage: int = Field(..., description="The amount of storage in GB")
    service_id: int = Field(..., description="The ID of the service")


class ServerOfferCreateSchema(BaseModel):
    price: float = Field(..., description="The price of the server offer")
    currency: str = Field(..., description="The currency of the server offer")
    cpu: int = Field(..., description="The number of CPU cores")
    memory: int = Field(..., description="The amount of memory in MB")
    storage: int = Field(..., description="The amount of storage in GB")
    service_id: int = Field(..., description="The ID of the service")


class ServerOfferUpdateSchema(BaseModel):
    price: float | None = Field(default=None, description="The price of the server offer")
    currency: str | None = Field(default=None, description="The currency of the server offer")
    cpu: int | None = Field(default=None, description="The number of CPU cores")
    memory: int | None = Field(default=None, description="The amount of memory in MB")
    storage: int | None = Field(default=None, description="The amount of storage in GB")
    service_id: int | None = Field(default=None, description="The ID of the service")
