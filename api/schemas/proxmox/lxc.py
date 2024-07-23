from enum import Enum
from pydantic import BaseModel, Field


class LXCStatus(str, Enum):
    RUNNING = "running"
    STOPPED = "stopped"


class LXCConfig(BaseModel):
    vmid: int = Field(..., description="The ID of the LXC container")
    hostname: str = Field(..., description="The name of the LXC container")
    ostemplate: str = Field(..., description="The OS template of the LXC container")
    password: str = Field(..., description="The password of the LXC container")
    memory: int = Field(..., description="The memory of the LXC container")
    swap: int = Field(..., description="The swap of the LXC container")
    net0: str = Field(..., description="The network interface of the LXC container")
    ssh_public_keys: str = Field(..., description="The SSH public keys of the LXC container")
    rootfs: str = Field(..., description="The rootfs of the LXC container")
    storage: str = Field(..., description="The storage of the LXC container")


class LXCStatusChange(str, Enum):
    START = "start"
    STOP = "stop"
    SHUTDOWN = "shutdown"
    REBOOT = "reboot"
