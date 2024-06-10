from pydantic import BaseModel


class StorageSchema(BaseModel):
    id: int | None = None
    size: str
    type: str
    cloud_id: int


class StorageCreateSchema(BaseModel):
    size: str
    type: str
    cloud_id: int


class StorageUpdateSchema(BaseModel):
    size: str | None = None
    type: str | None = None
    cloud_id: int | None = None
