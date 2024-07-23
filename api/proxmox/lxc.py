from typing import Optional
from fastapi import HTTPException, status
from .init import prox
from utils.logs import logger
from schemas.proxmox.lxc import LXCConfig, LXCStatusChange


def get_lxc(proxmox_node: str, vmid: Optional[int] = None):
    try:
        if vmid:
            logger.info(f"Retrieving LXC container config with vmid {vmid} for node {proxmox_node}")
            return prox.nodes(proxmox_node).lxc(vmid).config.get()
        else:
            logger.info(f"Retrieving all LXC containers for node {proxmox_node}")
            return prox.nodes(proxmox_node).lxc.get()
    except Exception as e:
        logger.error(f"Error retrieving LXC containers: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error retrieving LXC containers: {e}")


def create_lxc(proxmox_node: str, lxc_config: LXCConfig):
    try:
        logger.info(f"Creating LXC container for node {proxmox_node}")
        params = {
            "vmid": lxc_config.vmid,
            "hostname": lxc_config.hostname,
            "ostemplate": lxc_config.ostemplate,
            "password": lxc_config.password,
            "memory": lxc_config.memory,
            "swap": lxc_config.swap,
            "net0": lxc_config.net0,
            "ssh-public-keys": lxc_config.ssh_public_keys,
            "rootfs": lxc_config.rootfs,
            "storage": lxc_config.storage,
            "onboot": 1,
            "start": 1,
        }
        return prox.nodes(proxmox_node).lxc.post(**params)
    except Exception as e:
        logger.error(f"Error creating LXC container: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating LXC container: {e}")


def delete_lxc(proxmox_node: str, vmid: int):
    try:
        logger.info(f"Deleting LXC container with vmid: {vmid} for node: {proxmox_node}")
        params = {
            "destroy-unreferenced-disks": 1,
            "purge": 1,
            "force": 1,
        }
        return prox.nodes(proxmox_node).lxc(vmid).delete(**params)
    except Exception as e:
        logger.error(f"Error deleting LXC container: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error deleting LXC container: {e}")


def change_status_lxc(proxmox_node: str, vmid: int, lxc_status: LXCStatusChange):
    match lxc_status:
        case LXCStatusChange.START:
            logger.info(f"Starting LXC container with vmid: {vmid} for node: {proxmox_node}")
            try:
                return prox.nodes(proxmox_node).lxc(vmid).status.start.post()
            except Exception as e:
                logger.error(f"Error starting LXC container: {e}")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error starting LXC container: {e}")
        case LXCStatusChange.STOP:
            logger.info(f"Stopping LXC container with vmid: {vmid} for node: {proxmox_node}")
            try:
                return prox.nodes(proxmox_node).lxc(vmid).status.stop.post()
            except Exception as e:
                logger.error(f"Error stopping LXC container: {e}")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error stopping LXC container: {e}")
        case LXCStatusChange.SHUTDOWN:
            logger.info(f"Shutting down LXC container with vmid: {vmid} for node: {proxmox_node}")
            try:
                return prox.nodes(proxmox_node).lxc(vmid).status.shutdown.post()
            except Exception as e:
                logger.error(f"Error shutting down LXC container: {e}")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error shutting down LXC container: {e}")
        case LXCStatusChange.REBOOT:
            logger.info(f"Rebooting LXC container with vmid: {vmid} for node: {proxmox_node}")
            try:
                return prox.nodes(proxmox_node).lxc(vmid).status.reboot.post()
            except Exception as e:
                logger.error(f"Error rebooting LXC container: {e}")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error rebooting LXC container: {e}")
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid status: {status}")
