from pydantic import BaseModel, Field


class SshKeySchema(BaseModel):
    id: int | None = None
    name: str = Field(..., description="The name of the ssh key")
    public_key: str = Field(..., description="The public key of the ssh key")
    project_id: int = Field(..., description="The id of the project")


class SshKeyCreateSchema(BaseModel):
    name: str = Field(..., description="The name of the ssh key")
    public_key: str = Field(..., description="The public key of the ssh key")
    project_id: int = Field(..., description="The id of the project")


class SshKeyUpdateSchema(BaseModel):
    name: str | None = Field(default=None, description="The name of the ssh key")
    public_key: str | None = Field(default=None, description="The public key of the ssh key")
    project_id: int | None = Field(default=None, description="The id of the project")
