from sqlalchemy import Column, Integer, String, DateTime, LargeBinary
from datetime import datetime
from app.database import Base

class AnimalPicture(Base):
    __tablename__ = "animal_pictures"
    
    id = Column(Integer, primary_key=True, index=True)
    animal_type = Column(String, index=True)  # cat, dog, or bear
    image_data = Column(LargeBinary)  # Store image as binary
    image_url = Column(String)  # Original URL
    width = Column(Integer)
    height = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<AnimalPicture(id={self.id}, type={self.animal_type}, created={self.created_at})>"
