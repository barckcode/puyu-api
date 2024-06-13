from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.config import Base, engine


class VpcModel(Base):
    __tablename__ = 'aws_vpc'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    aws_resource_id = Column(String, unique=True, nullable=False)
    cidr_block = Column(String, nullable=False)
    region_cloud_id = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)

    project = relationship('ProjectModel', back_populates='aws_vpc')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "aws_resource_id": self.aws_resource_id,
            "cidr_block": self.cidr_block,
            "region_cloud_id": self.region_cloud_id,
            "project_id": self.project_id,
        }


class SubnetModel(Base):
    __tablename__ = 'aws_subnet'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    aws_resource_id = Column(String, unique=True, nullable=False)
    cidr_block = Column(String, nullable=False)
    aws_vpc_id = Column(String, nullable=False)
    availability_zone = Column(String, nullable=False)
    region_cloud_id = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)

    project = relationship('ProjectModel', back_populates='aws_subnet')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "aws_resource_id": self.aws_resource_id,
            "cidr_block": self.cidr_block,
            "aws_vpc_id": self.aws_vpc_id,
            "availability_zone": self.availability_zone,
            "region_cloud_id": self.region_cloud_id,
            "project_id": self.project_id,
        }


Base.metadata.create_all(engine)
