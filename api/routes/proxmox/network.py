from fastapi import APIRouter, Path, Query, status, HTTPException, Path
from fastapi.responses import JSONResponse, Response
from typing import Optional
from proxmox.network import get_network_devices, create_network_devices, reload_network_config, remove_network_device


network_devices = APIRouter()


@network_devices.get(
    "/proxmox/{proxmox_node}/network",
    tags=["proxmox"],
    summary="Get the network interfaces for a given node",
    description="Get the network interfaces for a given node, optionally filtered by interface type",
)
def get_network(
    proxmox_node: str = Path(..., description="The name of the node to retrieve the interfaces from (e.g., 'pve', 'node01')"),
    interface_type: Optional[str] = Query(None, description="Filter interfaces by type (e.g., 'bridge', 'vlan', 'eth')")
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid interface type. Must be 'vlan', 'bridge', or 'alias'.")
    interfaces = get_network_devices(proxmox_node, interface_type=interface_type)
    valid_fields = {
        "vlan": ["vlan-id", "iface", "type"],
        "bridge": ["iface", "cidr", "type", "bridge_ports"],
        "alias": ["iface", "cidr", "type"]
    }
    if fields:
        requested_fields = fields.split(',')
        invalid_fields = [field for field in requested_fields if field not in valid_fields[interface_type]]
        if invalid_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid fields for {interface_type} interface: {', '.join(invalid_fields)}. Valid fields are: {', '.join(valid_fields[interface_type])}"
            )
        fields_to_include = requested_fields
    else:
        fields_to_include = valid_fields[interface_type]
    filtered_interfaces = [
        {field: interface.get(field) for field in fields_to_include if interface.get(field) is not None}
        for interface in interfaces
    ]
    filtered_interfaces = [interface for interface in filtered_interfaces if interface]
    if not filtered_interfaces:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return JSONResponse(content=filtered_interfaces)


@network_devices.post(
    "/proxmox/{proxmox_node}/network",
    tags=["proxmox"],
    summary="Create a new network interface for a given node",
    description="Create a new network interface for a given node with specific fields",
)
def create_network(
    proxmox_node: str = Path(..., description="The name of the node to create the interface on (e.g., 'pve', 'node01')"),
    iface: str = Query(..., description="The name of the interface to create (e.g., 'eth0', 'enp3s0f1.101')"),
    type: str = Query(..., description="The type of interface to create (e.g., 'vlan', 'bridge', 'alias')"),
    vlan_raw_device: Optional[str] = Query(None, description="The raw device to use for VLAN creation (e.g., 'enp3s0f1, eth0')"),
    bridge_ports: Optional[str] = Query(None, description="The bridge ports to use for bridge creation (e.g., 'enp3s0f1.101, eth0.105')"),
    address: Optional[str] = Query(None, description="The IP address to use for the interface (e.g., '10.10.0.1')"),
    netmask: Optional[str] = Query(None, description="The netmask to use for the interface (e.g., '255.255.255.192')")
):
    create_network_devices(proxmox_node, iface, type, vlan_raw_device, bridge_ports, address, netmask)
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
