from pydantic import BaseModel


class CloudSchema(BaseModel):
    id: int | None = None
    name: str


class CloudCreateSchema(BaseModel):
    name: str


class CloudUpdateSchema(BaseModel):
    name: str | None = None
