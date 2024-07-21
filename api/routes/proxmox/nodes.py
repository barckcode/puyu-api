from fastapi import APIRouter
from proxmox.nodes import get_nodes

pve_nodes = APIRouter()

@pve_nodes.get(
    "/proxmox/nodes",
    tags=["proxmox"],
    summary="Get the nodes",
    description="Get the nodes",
)
def read_root():
    return get_nodes()
