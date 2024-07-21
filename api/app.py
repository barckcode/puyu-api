from fastapi import FastAPI
from routes.proxmox.nodes import pve_nodes
from routes.proxmox.network import network_devices

app = FastAPI(
    title="Puyu API",
    description="Helmcode Cloud API",
    version="0.0.1",
    openapi_tags=[
        {
            "name": "proxmox",
            "description": "Proxmox API",
        }
    ],
)

app.include_router(pve_nodes)
app.include_router(network_devices)
