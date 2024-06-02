from pydantic import BaseModel


class ProjectUserSchema(BaseModel):
    id: int | None = None
    sub: str
    project_id: int
