from pydantic import BaseModel


class AmiSchema(BaseModel):
    id: int | None = None
    distribution: str
    version: str
    ami_aws_id: str
    region_id: int


class AmiCreateSchema(BaseModel):
    distribution: str
    version: str
    ami_aws_id: str
    region_id: int


class AmiUpdateSchema(BaseModel):
    distribution: str | None = None
    version: str | None = None
    ami_aws_id: str | None = None
    region_id: int | None = None
