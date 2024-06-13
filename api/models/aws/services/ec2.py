from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.config import Base, engine


class KeyPairModel(Base):
    __tablename__ = 'aws_key_pair'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    region_cloud_id = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)

    project = relationship('ProjectModel', back_populates='aws_key_pair')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "region_cloud_id": self.region_cloud_id,
            "project_id": self.project_id,
        }


Base.metadata.create_all(engine)
