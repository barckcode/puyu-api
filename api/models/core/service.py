from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.config import Base, engine


class ServiceModel(Base):
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    cloud_id = Column(Integer, ForeignKey('cloud.id'), nullable=False)

    cloud = relationship('CloudModel', back_populates='service')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "cloud_id": self.cloud_id,
        }

Base.metadata.create_all(engine)
