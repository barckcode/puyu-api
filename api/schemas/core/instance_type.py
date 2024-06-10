from pydantic import BaseModel


class InstanceTypeSchema(BaseModel):
    id: int | None = None
    cpu: str
    memory: str
    instance_type_cloud_id: str
    cloud_id: int


class InstanceTypeCreateSchema(BaseModel):
    cpu: str
    memory: str
    instance_type_cloud_id: str
    cloud_id: int


class InstanceTypeUpdateSchema(BaseModel):
    cpu: str | None = None
    memory: str | None = None
    instance_type_cloud_id: str | None = None
    cloud_id: int | None = None
