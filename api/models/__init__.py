from db.config import Base, engine

# Auth Models
from .auth.user_project import UserProjectModel
from .auth.ssh_key import SshKeyModel


# Core Models
from .core.project import ProjectModel
from .core.region import RegionModel
from .core.service import ServiceModel
from .core.region_service import RegionServiceModel

# Business Models
from .business.server_offer import ServerOfferModel

# Server Models
from .servers.image import ServerImageModel
from .servers.region_image import RegionImageModel
from .servers.node import ProxNodeModel

# Networking Models
from .networking.vlan import ProxVlanModel

Base.metadata.create_all(engine)
