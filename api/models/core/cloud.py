from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from db.config import Base, engine


class CloudModel(Base):
    __tablename__ = 'cloud'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    service = relationship('ServiceModel', back_populates='cloud')
    region = relationship('RegionModel', back_populates='cloud')
    instance_type = relationship('InstanceTypeModel', back_populates='cloud')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

Base.metadata.create_all(engine)
