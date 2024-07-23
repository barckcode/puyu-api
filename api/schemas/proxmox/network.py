from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class NetworkType(str, Enum):
    VLAN = "vlan"
    BRIDGE = "bridge"
    ALIAS = "alias"
    BOND = "bond"
    ETHERNET = "eth"


class CreateNetworkRequest(BaseModel):
    iface: str = Field(..., description="The name of the interface to create (e.g., 'eth0', 'enp3s0f1.101')")
    type: str = Field(..., description="The type of interface to create (e.g., 'vlan', 'bridge', 'alias')")
    vlan_raw_device: Optional[str] = Field(None, description="The raw device to use for VLAN creation (e.g., 'enp3s0f1, eth0')")
    bridge_ports: Optional[str] = Field(None, description="The bridge ports to use for bridge creation (e.g., 'enp3s0f1.101, eth0.105')")
    address: Optional[str] = Field(None, description="The IP address to use for the interface (e.g., '10.10.0.1')")
    netmask: Optional[str] = Field(None, description="The netmask to use for the interface (e.g., '255.255.255.192')")

    class Config:
        from_attributes = True
