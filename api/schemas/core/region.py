from pydantic import BaseModel


class RegionSchema(BaseModel):
    id: int | None = None
    name: str
    region_cloud_id: str
    cloud_id: int


class RegionCreateSchema(BaseModel):
    name: str
    region_cloud_id: str
    cloud_id: int


class RegionUpdateSchema(BaseModel):
    name: str | None = None
    region_cloud_id: str | None = None
    cloud_id: int | None = None
