from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.config import Base


class RegionImageModel(Base):
    __tablename__ = 'region_image'
    id = Column(Integer, primary_key=True)
    region_id = Column(Integer, ForeignKey('regions.id'), nullable=False)
    image_id = Column(Integer, ForeignKey('server_images.id'), nullable=False)

    region = relationship('RegionModel', back_populates='server_images')
    server_images = relationship('ServerImageModel', back_populates='regions')

    def to_dict(self):
        return {
            "id": self.id,
            "region_id": self.region_id,
            "image_id": self.image_id,
        }
