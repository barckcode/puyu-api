from fastapi import APIRouter, Path, Query, Body, status
from fastapi.responses import JSONResponse, Response
from typing import Optional
from proxmox.lxc import get_lxc, create_lxc, delete_lxc, change_status_lxc
from utils.size_changes import bytes_to_gb
from utils.logs import logger
from schemas.proxmox.lxc import LXCStatus, LXCConfig, LXCStatusChange


lxc_containers = APIRouter()


@lxc_containers.get(
    "/proxmox/{proxmox_node}/lxc",
    tags=["proxmox"],
    summary="Get all LXC containers for a given node",
    description="Get all LXC containers for a given node, optionally filtered by status",
)
def get_lxc_containers(
    proxmox_node: str = Path(..., description="The name of the Proxmox node"),
    lxc_status: Optional[LXCStatus] = Query(None, description="Filter containers by status (running or stopped)")
):
    containers = get_lxc(proxmox_node)
    logger.info(f"Retrieved {len(containers)} containers from Proxmox")
    logger.info(f"Filtering with status: {lxc_status}")
    filtered_containers = []
    for container in containers:
        container_status = container["status"].lower()
        if lxc_status is None or container_status == lxc_status:
            filtered_containers.append({
                "name": container["name"],
                "vmid": container["vmid"],
                "type": container["type"],
                "status": container_status,
                "cpus": container["cpus"],
                "maxmem_gb": bytes_to_gb(container["maxmem"]),
                "maxdisk_gb": bytes_to_gb(container["maxdisk"])
            })
    if not filtered_containers:
        logger.info("No containers match the filter, returning 204")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return JSONResponse(content=filtered_containers, status_code=status.HTTP_200_OK)


@lxc_containers.get(
    "/proxmox/{proxmox_node}/lxc/{vmid}",
    tags=["proxmox"],
    summary="Get specific information for a LXC container",
    description="Get name, architecture, OS type, and network information for a specific LXC container",
)
def get_lxc_container_config(
    proxmox_node: str = Path(..., description="The name of the Proxmox node"),
    vmid: int = Path(..., description="The ID of the LXC container")
):
    container = get_lxc(proxmox_node, vmid)
    net0_info = dict(item.split("=") for item in container["net0"].split(","))
    filtered_container = {
        "name": container["hostname"],
        "arch": container["arch"],
        "ostype": container["ostype"],
        "iface": net0_info.get("name"),
        "bridge": net0_info.get("bridge"),
        "gateway": net0_info.get("gw"),
        "address": net0_info.get("ip"),
    }
    return JSONResponse(content=filtered_container, status_code=status.HTTP_200_OK)


@lxc_containers.post(
    "/proxmox/{proxmox_node}/lxc",
    tags=["proxmox"],
    summary="Create a new LXC container",
    description="Create a new LXC container",
)
def create_lxc_container(
    proxmox_node: str = Path(..., description="The name of the Proxmox node"),
    lxc_config: LXCConfig = Body(..., description="The configuration of the LXC container")
):
    create_lxc(proxmox_node, lxc_config)
    return Response(status_code=status.HTTP_201_CREATED)


@lxc_containers.delete(
    "/proxmox/{proxmox_node}/lxc/{vmid}",
    tags=["proxmox"],
    summary="Delete a LXC container",
    description="Delete a LXC container",
)
def delete_lxc_container(
    proxmox_node: str = Path(..., description="The name of the Proxmox node"),
    vmid: int = Path(..., description="The ID of the LXC container")
):
    delete_lxc(proxmox_node, vmid)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@lxc_containers.post(
    "/proxmox/{proxmox_node}/lxc/{vmid}",
    tags=["proxmox"],
    summary="Change the status of a LXC container",
    description="Change the status of a LXC container",
)
def change_status_lxc_container(
    proxmox_node: str = Path(..., description="The name of the Proxmox node"),
    vmid: int = Path(..., description="The ID of the LXC container"),
    lxc_status: LXCStatusChange = Query(..., description="The new status of the LXC container")
):
    change_status_lxc(proxmox_node, vmid, lxc_status)
    return Response(status_code=status.HTTP_200_OK)
