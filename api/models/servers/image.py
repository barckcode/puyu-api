from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.config import Base


class ServerImageModel(Base):
    __tablename__ = 'server_images'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    source = Column(String, nullable=False)
    logo = Column(String, nullable=False)
    available = Column(Boolean, nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)

    service = relationship('ServiceModel', back_populates='server_images')
    regions = relationship('RegionImageModel', back_populates='server_images')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "source": self.source,
            "logo": self.logo,
            "available": self.available,
            "service_id": self.service_id,
            "regions": [rs.region_id for rs in self.regions]
        }
