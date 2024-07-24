from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.config import Base


class RegionServiceModel(Base):
    __tablename__ = 'region_service'
    id = Column(Integer, primary_key=True)
    region_id = Column(Integer, ForeignKey('regions.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)

    region = relationship('RegionModel', back_populates='services')
    service = relationship('ServiceModel', back_populates='regions')

    def to_dict(self):
        return {
            "id": self.id,
            "region_id": self.region_id,
            "service_id": self.service_id,
        }
