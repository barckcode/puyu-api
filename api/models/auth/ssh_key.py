from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.config import Base


class SshKeyModel(Base):
    __tablename__ = 'ssh_keys'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    public_key = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)

    project = relationship('ProjectModel', back_populates='ssh_key')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "public_key": self.public_key,
            "project_id": self.project_id,
        }
