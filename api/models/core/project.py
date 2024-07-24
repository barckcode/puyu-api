from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from db.config import Base, engine


class ProjectModel(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # project_user = relationship('UserProjectModel', back_populates='project')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

Base.metadata.create_all(engine)
