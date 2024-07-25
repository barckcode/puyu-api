from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship
from db.config import Base


class RegionModel(Base):
    __tablename__ = 'regions'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    logo = Column(String, nullable=False)
    available = Column(Boolean, nullable=False)

    services = relationship('RegionServiceModel', back_populates='region')
    server_images = relationship('RegionImageModel', back_populates='region')
    prox_nodes = relationship('ProxNodeModel', back_populates='region')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "logo": self.logo,
            "available": self.available,
        }
