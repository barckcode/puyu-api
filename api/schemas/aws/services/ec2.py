from pydantic import BaseModel


class KeyPairCreateSchema(BaseModel):
    name: str
    region_cloud_id: str
