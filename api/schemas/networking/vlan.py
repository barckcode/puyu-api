from pydantic import BaseModel, Field
from typing import Optional


class ProxVlanFilterParams(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    prox_node_id: Optional[int] = None


class ProxVlanSchema(BaseModel):
    id: int | None = None
    name: str = Field(..., description="The name of the node")
    prox_node_id: int = Field(..., description="The ID of the prox node the vlan belongs to")


class ProxVlanCreateSchema(BaseModel):
    name: str = Field(..., description="The name of the node")
    prox_node_id: int = Field(..., description="The ID of the prox node the vlan belongs to")


class ProxVlanUpdateSchema(BaseModel):
    name: str | None = Field(default=None, description="The name of the node")
    prox_node_id: int | None = Field(default=None, description="The ID of the prox node the vlan belongs to")
