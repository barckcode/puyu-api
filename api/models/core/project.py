from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from db.config import Base


class ProjectModel(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    user_project = relationship('UserProjectModel', back_populates='project')
    ssh_key = relationship('SshKeyModel', back_populates='project')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
