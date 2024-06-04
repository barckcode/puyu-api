from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.config import Base, engine


class AmiModel(Base):
    __tablename__ = 'aws_ami'
    id = Column(Integer, primary_key=True)
    distribution = Column(String, nullable=False)
    version = Column(String, nullable=False)
    ami_aws_id = Column(String, unique=True, nullable=False)
    region_id = Column(Integer, ForeignKey('aws_region.id'), nullable=False)

    region = relationship('RegionModel', back_populates='aws_ami')

    def to_dict(self):
        return {
            "id": self.id,
            "distribution": self.distribution,
            "version": self.version,
            "region": self.region,
            "ami_aws_id": self.ami_aws_id,
            "region_id": self.region_id,
        }

Base.metadata.create_all(engine)
