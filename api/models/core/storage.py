from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.config import Base, engine


class StorageModel(Base):
    __tablename__ = 'aws_storage'
    id = Column(Integer, primary_key=True)
    size = Column(String, nullable=False)
    type = Column(String, nullable=False)
    cloud_id = Column(Integer, ForeignKey('cloud.id'), nullable=False)

    cloud = relationship('CloudModel', back_populates='storage')

    def to_dict(self):
        return {
            "id": self.id,
            "size": self.size,
            "type": self.type,
            "cloud_id": self.cloud_id,
            "cloud": self.cloud.to_dict() if self.cloud else None
        }

Base.metadata.create_all(engine)
