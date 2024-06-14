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


class SecurityGroupModel(Base):
    __tablename__ = 'aws_security_group'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    aws_resource_id = Column(String, nullable=False)
    aws_vpc_id = Column(String, nullable=False)
    region_cloud_id = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)

    project = relationship('ProjectModel', back_populates='aws_security_group')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "aws_resource_id": self.aws_resource_id,
            "aws_vpc_id": self.aws_vpc_id,
            "region_cloud_id": self.region_cloud_id,
            "project_id": self.project_id,
        }


class SecurityGroupRuleModel(Base):
    __tablename__ = 'aws_security_group_rule'
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    aws_resource_id = Column(String, nullable=False)
    aws_security_group_id = Column(String, nullable=False)
    port = Column(Integer, nullable=False)
    protocol = Column(String, nullable=False)
    cird_ip = Column(String, nullable=False)
    region_cloud_id = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)

    project = relationship('ProjectModel', back_populates='aws_security_group_rule')

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "aws_resource_id": self.aws_resource_id,
            "aws_security_group_id": self.aws_security_group_id,
            "port": self.port,
            "protocol": self.protocol,
            "cird_ip": self.cird_ip,
            "region_cloud_id": self.region_cloud_id,
            "project_id": self.project_id,
        }


class InstanceModel(Base):
    __tablename__ = 'aws_instance'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    aws_resource_id = Column(String, nullable=False)
    disk_size = Column(Integer, nullable=False)
    public_ip = Column(String, nullable=False)
    private_ip = Column(String, nullable=False)
    key_pair_name = Column(String, nullable=False)
    instance_type_cloud_id = Column(String, nullable=False)
    aws_ami_id = Column(String, nullable=False)
    aws_subnet_id = Column(String, nullable=False)
    aws_security_group_id = Column(String, nullable=False)
    region_cloud_id = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)

    project = relationship('ProjectModel', back_populates='aws_instance')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "aws_resource_id": self.aws_resource_id,
            "disk_size": self.disk_size,
            "public_ip": self.public_ip,
            "private_ip": self.private_ip,
            "key_pair_name": self.key_pair_name,
            "instance_type_cloud_id": self.instance_type_cloud_id,
            "aws_ami_id": self.aws_ami_id,
            "aws_subnet_id": self.aws_subnet_id,
            "aws_security_group_id": self.aws_security_group_id,
            "region_cloud_id": self.region_cloud_id,
            "project_id": self.project_id,
        }

Base.metadata.create_all(engine)
