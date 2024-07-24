from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship
from db.config import Base, engine


class RegionModel(Base):
    __tablename__ = 'regions'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    logo = Column(String, nullable=False)
    available = Column(Boolean, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "logo": self.logo,
            "available": self.available,
        }

Base.metadata.create_all(engine)
