from pydantic import BaseModel, Field


class ProxNodeSchema(BaseModel):
    id: int | None = None
    name: str = Field(..., description="The name of the node")
    private_network_interface: str = Field(..., description="The private network interface of the node")
    public_network_interface: str = Field(..., description="The public network interface of the node")
    region_id: int = Field(..., description="The ID of the region the node belongs to")


class ProxNodeCreateSchema(BaseModel):
    name: str = Field(..., description="The name of the node")
    private_network_interface: str = Field(..., description="The private network interface of the node")
    public_network_interface: str = Field(..., description="The public network interface of the node")
    region_id: int = Field(..., description="The ID of the region the node belongs to")


class ProxNodeUpdateSchema(BaseModel):
    name: str | None = Field(default=None, description="The name of the node")
    private_network_interface: str | None = Field(default=None, description="The private network interface of the node")
    public_network_interface: str | None = Field(default=None, description="The public network interface of the node")
    region_id: int | None = Field(default=None, description="The ID of the region the node belongs to")
