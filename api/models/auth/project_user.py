from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.config import Base, engine


class ProjectUserModel(Base):
    __tablename__ = 'project_user'
    id = Column(Integer, primary_key=True)
    sub = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)

    project = relationship('ProjectModel', back_populates='project_user')

    def to_dict(self):
        return {
            "id": self.id,
            "sub": self.sub,
            "project_id": self.project_id,
        }

Base.metadata.create_all(engine)
