import urllib3
from proxmoxer import ProxmoxAPI
from config.vars import env

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

prox = ProxmoxAPI(
    host=env["PVE_HOST"],
    user=env["PVE_USER"],
    token_name=env["PVE_TOKEN_NAME"],
    token_value=env["PVE_TOKEN_VALUE"],
    verify_ssl=False,
    timeout=60
)
