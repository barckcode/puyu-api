from fastapi import APIRouter, status, HTTPException, Path, Body, Query
from fastapi.responses import JSONResponse, Response
from typing import Optional
from proxmox.network import get_network_devices, create_network_devices, reload_network_config, remove_network_device
from utils.logs import logger
from schemas.proxmox.network import NetworkType, CreateNetworkRequest


network_devices = APIRouter()


@network_devices.get(
    "/proxmox/{proxmox_node}/network",
    tags=["proxmox"],
    summary="Get the network interfaces for a given node",
    description="Get the network interfaces for a given node, optionally filtered by interface type",
)
def get_network(
    proxmox_node: str = Path(..., description="The name of the node to retrieve the interfaces from (e.g., 'pve', 'node01')"),
    interface_type: Optional[NetworkType] = Query(None, description="Filter interfaces by type")
):
    network_devices = get_network_devices(proxmox_node)
    if interface_type:
        filtered_devices = [device for device in network_devices if device.get('type') == interface_type]
        return JSONResponse(content=filtered_devices)
    return JSONResponse(content=network_devices)


@network_devices.get(
    "/proxmox/{proxmox_node}/network/{interface_type}",
    tags=["proxmox"],
    summary="Get specific network interfaces for a given node",
    description="Get network interfaces of a specific type (vlan, bridge, alias) for a given node with specific fields",
)
def get_specific_interfaces(
    proxmox_node: str = Path(..., description="The name of the node to retrieve the interfaces from (e.g., 'pve', 'node01')"),
    interface_type: str = Path(..., description="Type of interface to retrieve (vlan, bridge, alias)"),
    fields: Optional[str] = Query(None, description="Comma-separated list of fields to include in the response")
):
    if interface_type not in ["vlan", "bridge", "alias"]:
        logger.error(f"Invalid interface type: {interface_type}. Must be 'vlan', 'bridge', or 'alias'.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid interface type. Must be 'vlan', 'bridge', or 'alias'.")
    interfaces = get_network_devices(proxmox_node, interface_type=interface_type)
    valid_fields = {
        "vlan": ["vlan-id", "iface", "type"],
        "bridge": ["iface", "cidr", "type", "bridge_ports"],
        "alias": ["iface", "cidr", "type"]
    }
    if fields:
        logger.info(f"Requested fields: {fields}")
        requested_fields = fields.split(',')
        invalid_fields = [field for field in requested_fields if field not in valid_fields[interface_type]]
        if invalid_fields:
            logger.error(f"Invalid fields for {interface_type} interface: {', '.join(invalid_fields)}. Valid fields are: {', '.join(valid_fields[interface_type])}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid fields for {interface_type} interface: {', '.join(invalid_fields)}. Valid fields are: {', '.join(valid_fields[interface_type])}"
            )
        fields_to_include = requested_fields
    else:
        logger.info(f"No fields requested. Using all fields for {interface_type} interface.")
        fields_to_include = valid_fields[interface_type]
    filtered_interfaces = [
        {field: interface.get(field) for field in fields_to_include if interface.get(field) is not None}
        for interface in interfaces
    ]
    logger.info(f"Filtered interfaces: {filtered_interfaces}")
    filtered_interfaces = [interface for interface in filtered_interfaces if interface]
    if not filtered_interfaces:
        logger.info(f"No {interface_type} interfaces found.")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return JSONResponse(content=filtered_interfaces)


@network_devices.post(
    "/proxmox/{proxmox_node}/network",
    tags=["proxmox"],
    summary="Create a new network interface for a given node",
    description="Create a new network interface for a given node with specific fields",
)
def create_network(
    network_data: CreateNetworkRequest = Body(...),
    proxmox_node: str = Path(..., description="The name of the node to create the interface on"),
):
    create_network_devices(
        proxmox_node,
        network_data.iface,
        network_data.type,
        network_data.vlan_raw_device,
        network_data.bridge_ports,
        network_data.address,
        network_data.netmask
    )
    reload_network_config(proxmox_node)
    return JSONResponse(content={"message": "Network device created successfully"}, status_code=status.HTTP_201_CREATED)


@network_devices.delete(
    "/proxmox/{proxmox_node}/network/{interface_name}",
    tags=["proxmox"],
    summary="Delete a network interface for a given node",
    description="Delete a network interface for a given node",
)
def remove_network(
    proxmox_node: str = Path(..., description="The name of the node to delete the interface from (e.g., 'pve', 'node01')"),
    interface_name: str = Path(..., description="The name of the interface to delete (e.g., 'eth0', 'enp3s0f1.101')")
):
    remove_network_device(proxmox_node, interface_name)
    reload_network_config(proxmox_node)
    return JSONResponse(content={"message": "Network device removed successfully"}, status_code=status.HTTP_200_OK)
