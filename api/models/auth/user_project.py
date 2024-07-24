from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.config import Base, engine


class UserProjectModel(Base):
    __tablename__ = 'user_project'
    id = Column(Integer, primary_key=True)
    sub = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)

    project = relationship('ProjectsModel', back_populates='project_user')

    def to_dict(self):
        return {
            "id": self.id,
            "sub": self.sub,
            "project_id": self.project_id,
        }

Base.metadata.create_all(engine)
