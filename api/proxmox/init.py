from proxmoxer import ProxmoxAPI
from config.vars import env


prox = ProxmoxAPI(
    host=env["PVE_HOST"],
    user=env["PVE_USER"],
    token_name=env["PVE_TOKEN_NAME"],
    token_value=env["PVE_TOKEN_VALUE"],
    verify_ssl=False,
    timeout=60
)
