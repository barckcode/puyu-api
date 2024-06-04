from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from db.config import Base, engine


class RegionModel(Base):
    __tablename__ = 'aws_region'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    region_aws_id = Column(String, unique=True, nullable=False)

    ami = relationship('AmiModel', back_populates='region')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "region_aws_id": self.region_aws_id,
        }

Base.metadata.create_all(engine)
