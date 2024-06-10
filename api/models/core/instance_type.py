from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.config import Base, engine


class InstanceTypeModel(Base):
    __tablename__ = 'instance_type'
    id = Column(Integer, primary_key=True)
    cpu = Column(String, nullable=False)
    memory = Column(String, nullable=False)
    instance_type_cloud_id = Column(String, unique=True, nullable=False)
    cloud_id = Column(Integer, ForeignKey('cloud.id'), nullable=False)

    cloud = relationship('CloudModel', back_populates='instance_type')

    def to_dict(self):
        return {
            "id": self.id,
            "cpu": self.cpu,
            "memory": self.memory,
            "instance_type_cloud_id": self.instance_type_cloud_id,
            "cloud_id": self.cloud_id,
            "cloud": self.cloud.to_dict() if self.cloud else None
        }

Base.metadata.create_all(engine)
