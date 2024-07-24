from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.config import Base


class ServerOfferModel(Base):
    __tablename__ = 'server_offers'
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    cpu = Column(Integer, nullable=False)
    memory = Column(Integer, nullable=False)
    storage = Column(Integer, nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)

    service = relationship('ServiceModel', back_populates='server_offers')

    def to_dict(self):
        return {
            "id": self.id,
            "price": self.price,
            "currency": self.currency,
            "cpu": self.cpu,
            "memory": self.memory,
            "storage": self.storage,
            "service_id": self.service_id,
        }
