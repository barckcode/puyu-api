from pydantic import BaseModel


class ProjectSchema(BaseModel):
    id: int | None = None
    name: str


class ProjectCreateSchema(BaseModel):
    name: str


class ProjectUpdateSchema(BaseModel):
    name: str | None = None
