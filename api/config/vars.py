import os


env = {
    # Proxmox
    "PVE_HOST": os.environ.get("PVE_HOST"),
    "PVE_USER": os.environ.get("PVE_USER"),
    "PVE_TOKEN_NAME": os.environ.get("PVE_TOKEN_NAME"),
    "PVE_TOKEN_VALUE": os.environ.get("PVE_TOKEN_VALUE"),
    "PVE_NODE": os.environ.get("PVE_NODE"),
    # Database
    "DATABASE_CONNECTION_STRING": os.environ.get("DATABASE_CONNECTION_STRING")
}
