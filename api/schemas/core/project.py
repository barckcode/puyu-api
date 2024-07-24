from pydantic import BaseModel, Field


class ProjectSchema(BaseModel):
    id: int | None = None
    name: str = Field(..., description="The name of the project")


class ProjectCreateSchema(BaseModel):
    name: str = Field(..., description="The name of the project")


class ProjectUpdateSchema(BaseModel):
    name: str | None = Field(default=None, description="The name of the project")
