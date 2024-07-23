from typing import Optional
from fastapi import HTTPException, status
from .init import prox
from utils.logs import logger


def get_network_devices(proxmox_node: str, interface_type: Optional[str] = None):
    if interface_type:
        try:
            logger.info(f"Getting network devices for node {proxmox_node} with type {interface_type}")
            return prox.nodes(proxmox_node).network.get(type=interface_type)
        except Exception as e:
            logger.error(f"Error getting network devices: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error getting network devices: {e}")
    try:
        logger.info(f"Getting all network devices for node {proxmox_node}")
        return prox.nodes(proxmox_node).network.get()
    except Exception as e:
        logger.error(f"Error getting network devices: {e}")
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
    logger.info(f"Creating network device with type {type}")
    match type:
        case "vlan":
            params = {
                "iface": iface,
                "type": type,
                "vlan-raw-device": vlan_raw_device,
                "autostart": 1
            }
            try:
                logger.info(f"Creating VLAN with params: {params}")
                return prox.nodes(proxmox_node).network.post(**params)
            except Exception as e:
                logger.error(f"Error creating VLAN: {e}")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating VLAN: {e}")
        case "bridge":
            try:
                logger.info(f"Creating bridge with params: {params}")
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
                logger.error(f"Error creating bridge: {e}")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating bridge: {e}")
        case "alias":
            try:
                logger.info(f"Creating alias with params: {params}")
                return prox.nodes(proxmox_node).network.post(
                    iface=iface,
                    type=type,
                    address=address,
                    netmask=netmask,
                    autostart=1
                )
            except Exception as e:
                logger.error(f"Error creating alias: {e}")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating alias: {e}")
        case _:
            logger.error(f"Invalid interface type: {type}")
            raise ValueError(f"Invalid interface type: {type}")


def remove_network_device(proxmox_node: str, iface: str):
    try:
        logger.info(f"Removing network device with iface {iface}")
        return prox.nodes(proxmox_node).network(iface).delete()
    except Exception as e:
        logger.error(f"Error removing network device: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error removing network device: {e}")


def reload_network_config(proxmox_node: str):
    try:
        logger.info(f"Reloading network config for node {proxmox_node}")
        return prox.nodes(proxmox_node).network.put()
    except Exception as e:
        logger.error(f"Error reloading network config: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error reloading network config: {e}")
