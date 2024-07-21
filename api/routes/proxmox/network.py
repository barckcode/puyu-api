from fastapi import APIRouter

network_devices = APIRouter()

@network_devices.get(
    "/proxmox/network",
    tags=["proxmox"],
    summary="Get the network interfaces",
    description="Get the network interfaces",
)
def read_root():
    return {"message": "Hello World"}
