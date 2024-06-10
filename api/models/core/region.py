from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.config import Base, engine


class RegionModel(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    region_cloud_id = Column(String, unique=True, nullable=False)
    cloud_id = Column(Integer, ForeignKey('cloud.id'), nullable=False)

    cloud = relationship('CloudModel', back_populates='region')
    ami = relationship('AmiModel', back_populates='region')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "region_cloud_id": self.region_cloud_id,
            "cloud_id": self.cloud_id,
            "cloud": self.cloud.to_dict() if self.cloud else None
        }

Base.metadata.create_all(engine)
