from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.config import Base


class ProxVlanModel(Base):
    __tablename__ = 'prox_vlans'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    prox_node_id = Column(Integer, ForeignKey('prox_nodes.id'), nullable=False)

    prox_node = relationship('ProxNodeModel', back_populates='prox_vlans')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "prox_node_id": self.prox_node_id,
        }
