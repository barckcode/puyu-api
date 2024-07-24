import logging
from fastapi import FastAPI
from routes.proxmox.nodes import pve_nodes
from routes.proxmox.network import network_devices
from routes.proxmox.lxc import lxc_containers
from routes.core.project import project_router
from routes.core.region import region_router
from routes.core.service import service_router
from routes.auth.ssh_key import ssh_key_router
from routes.business.server_offer import server_offer_router
from routes.servers.image import server_image_router


logging.basicConfig(level=logging.INFO)


app = FastAPI(
    title="Puyu API",
    description="Helmcode Cloud API",
    version="0.0.1",
    openapi_tags=[
        {
            "name": "auth",
            "description": "Authentication API",
        },
        {
            "name": "proxmox",
            "description": "Proxmox API",
        },
        {
            "name": "core",
            "description": "Core API",
            "children": [
                {
                    "name": "project",
                    "description": "Handle Projects",
                },
                {
                    "name": "region",
                    "description": "Handle Regions",
                },
                {
                    "name": "service",
                    "description": "Handle Services",
                },
                {
                    "name": "ssh_key",
                    "description": "Handle SSH Keys",
                }
            ]
        },
        {
            "name": "business",
            "description": "Business API",
            "children": [
                {
                    "name": "server_offer",
                    "description": "Handle Server Offers",
                }
            ]
        },
        {
            "name": "servers",
            "description": "Servers API",
            "children": [
                {
                    "name": "image",
                    "description": "Handle Server Images",
                }
            ]
        }
    ],
)

app.include_router(pve_nodes)
app.include_router(network_devices)
app.include_router(lxc_containers)
app.include_router(project_router)
app.include_router(region_router)
app.include_router(service_router)
app.include_router(ssh_key_router)
app.include_router(server_offer_router)
app.include_router(server_image_router)
