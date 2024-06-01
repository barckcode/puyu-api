from pydantic import BaseModel


class ServiceSchema(BaseModel):
    id: int | None = None
    name: str
    cloud_id: int


class ServiceCreateSchema(BaseModel):
    name: str
    cloud_id: int


class ServiceUpdateSchema(BaseModel):
    name: str | None = None
    cloud_id: int | None = None
