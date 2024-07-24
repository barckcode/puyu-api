from db.config import Base, engine

# Auth Models
from .auth.user_project import UserProjectModel
from .auth.ssh_key import SshKeyModel


# Core Models
from .core.project import ProjectModel
from .core.region import RegionModel
from .core.service import ServiceModel
from .core.region_service import RegionServiceModel


Base.metadata.create_all(engine)
