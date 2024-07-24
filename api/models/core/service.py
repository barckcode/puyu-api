from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship
from db.config import Base


class ServiceModel(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    available = Column(Boolean, nullable=False, default=True)

    regions = relationship('RegionServiceModel', back_populates='service')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "available": self.available,
        }
