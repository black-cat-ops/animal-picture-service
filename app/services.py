import requests
from sqlalchemy.orm import Session
from app.models import AnimalPicture
from app.schemas import AnimalPictureRequest
import logging
import random
import time

logger = logging.getLogger(__name__)

# Animal picture API endpoints with fallbacks
ANIMAL_APIS = {
    "cat": [
        "https://cataas.com/cat?width={width}&height={height}&t={random}",
        "https://placekitten.com/{width}/{height}",
    ],
    "dog": [
        "https://place.dog/{width}/{height}",
        "https://placedog.net/{width}/{height}",
    ],
    "bear": [
        "https://placebear.com/{width}/{height}",
        "https://placebear.com/g/{width}/{height}",
    ]
}

class AnimalService:
    
    @staticmethod
    def fetch_image_with_fallback(animal_type: str, width: int, height: int) -> tuple:
        """
        Try multiple APIs with fallback support
        Returns: (image_data, image_url)
        """
        if animal_type not in ANIMAL_APIS:
            raise ValueError(f"Invalid animal type. Must be one of: {list(ANIMAL_APIS.keys())}")
        
        urls = ANIMAL_APIS[animal_type]
        last_error = None
        
        # Use timestamp for cache busting
        random_param = int(time.time() * 1000)
        
        for url_template in urls:
            try:
                image_url = url_template.format(
                    width=width, 
                    height=height,
                    random=random_param
                )
                logger.info(f"Attempting to fetch from: {image_url}")
                
                response = requests.get(image_url, timeout=10)
                response.raise_for_status()
                
                # Success!
                logger.info(f"Successfully fetched image from: {image_url}")
                return response.content, image_url
                
            except requests.RequestException as e:
                last_error = e
                logger.warning(f"Failed to fetch from {image_url}: {e}")
                continue
        
        # All URLs failed
        raise Exception(f"All image sources failed for {animal_type}. Last error: {str(last_error)}")
    
    @staticmethod
    def fetch_and_store_picture(
        animal_request: AnimalPictureRequest, 
        db: Session
    ) -> AnimalPicture:
        """
        Fetch a picture from external API and store in database
        """
        animal_type = animal_request.animal_type.lower()
        
        # Fetch image with fallback support
        # Let ValueError propagate for invalid animal types
        image_data, image_url = AnimalService.fetch_image_with_fallback(
            animal_type,
            animal_request.width,
            animal_request.height
        )
        
        # Store in database
        db_picture = AnimalPicture(
            animal_type=animal_type,
            image_data=image_data,
            image_url=image_url,
            width=animal_request.width,
            height=animal_request.height
        )
        
        db.add(db_picture)
        db.commit()
        db.refresh(db_picture)
        
        logger.info(f"Stored picture with ID: {db_picture.id}")
        return db_picture
    
    @staticmethod
    def get_latest_picture(db: Session) -> AnimalPicture:
        """
        Get the most recently stored picture
        """
        picture = db.query(AnimalPicture).order_by(
            AnimalPicture.created_at.desc()
        ).first()
        
        if not picture:
            raise ValueError("No pictures found in database")
        
        return picture
    
    @staticmethod
    def get_picture_by_id(picture_id: int, db: Session) -> AnimalPicture:
        """
        Get a specific picture by ID
        """
        picture = db.query(AnimalPicture).filter(
            AnimalPicture.id == picture_id
        ).first()
        
        if not picture:
            raise ValueError(f"Picture with ID {picture_id} not found")
        
        return picture
