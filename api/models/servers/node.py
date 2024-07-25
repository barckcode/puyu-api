from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.config import Base


class ProxNodeModel(Base):
    __tablename__ = 'prox_nodes'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    private_network_interface = Column(String, nullable=False)
    public_network_interface = Column(String, nullable=False)
    region_id = Column(Integer, ForeignKey('regions.id'), nullable=False)

    region = relationship('RegionModel', back_populates='prox_nodes')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "private_network_interface": self.private_network_interface,
            "public_network_interface": self.public_network_interface,
            "region_id": self.region_id,
        }
