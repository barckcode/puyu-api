from pydantic import BaseModel


class RegionSchema(BaseModel):
    id: int | None = None
    name: str
    region_aws_id: str
    cloud_id: int


class RegionCreateSchema(BaseModel):
    name: str
    region_aws_id: str
    cloud_id: int


class RegionUpdateSchema(BaseModel):
    name: str | None = None
    region_aws_id: str | None = None
    cloud_id: int | None = None
