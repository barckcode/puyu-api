from sqlalchemy import Column, String, Integer
from db.config import Base, engine


class CloudModel(Base):
    __tablename__ = 'cloud'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

Base.metadata.create_all(engine)
