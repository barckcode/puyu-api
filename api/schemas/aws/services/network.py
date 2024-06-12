from pydantic import BaseModel


class VpcCreateAwsSchema(BaseModel):
    name: str
    cidr_block: str
    region_cloud_id: str


class VpcCreateDbSchema(BaseModel):
    name: str
    aws_resource_id: str
    cidr_block: str
    region_cloud_id: str
