from typing import Optional
from fastapi import HTTPException, status
from .init import prox


def get_network_devices(proxmox_node: str, interface_type: Optional[str] = None):
    if interface_type:
        try:
            return prox.nodes(proxmox_node).network.get(type=interface_type)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error getting network devices: {e}")
    try:
        return prox.nodes(proxmox_node).network.get()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error getting network devices: {e}")


def create_network_devices(
        proxmox_node: str,
        iface: str,
        type: str,
        vlan_raw_device: Optional[str] = None,
        bridge_ports: Optional[str] = None,
        address: Optional[str] = None,
        netmask: Optional[str] = None
):
    match type:
        case "vlan":
            params = {
                "iface": iface,
                "type": type,
                "vlan-raw-device": vlan_raw_device,
                "autostart": 1
            }
            try:
                return prox.nodes(proxmox_node).network.post(**params)
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating VLAN: {e}")
        case "bridge":
            try:
                return prox.nodes(proxmox_node).network.post(
                    iface=iface,
                    type=type,
                    bridge_ports=bridge_ports,
                    address=address,
                    netmask=netmask,
                    bridge_vlan_aware=1,
                    autostart=1
                )
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating bridge: {e}")
        case "alias":
            try:
                return prox.nodes(proxmox_node).network.post(
                    iface=iface,
                    type=type,
                    address=address,
                    netmask=netmask,
                    autostart=1
                )
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating alias: {e}")
        case _:
            raise ValueError(f"Invalid interface type: {type}")


def reload_network_config(proxmox_node: str):
    try:
        return prox.nodes(proxmox_node).network.put()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error reloading network config: {e}")
