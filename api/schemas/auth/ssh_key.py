from pydantic import BaseModel


class SshKeySchema(BaseModel):
    id: int | None = None
    name: str
    public_key: str
    project_id: int


class SshKeyCreateSchema(BaseModel):
    name: str
    public_key: str
    project_id: int


class SshKeyUpdateSchema(BaseModel):
    name: str | None = None
    public_key: str | None = None
    project_id: int | None = None
