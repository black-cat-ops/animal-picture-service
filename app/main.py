from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text
from prometheus_client import Counter, Histogram, generate_latest
import logging
import io

from app.database import engine, get_db, Base
from app.models import AnimalPicture
from app.schemas import (
    AnimalPictureRequest, 
    AnimalPictureResponse, 
    HealthResponse
)
from app.services import AnimalService
from app.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A microservice for fetching and storing random animal pictures"
)

# Prometheus metrics
request_count = Counter(
    'app_requests_total', 
    'Total number of requests',
    ['method', 'endpoint']
)
request_duration = Histogram(
    'app_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)

@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Serve simple UI
    """
    with open("ui/index.html", "r") as f:
        return f.read()

@app.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint
    """
    try:
        # Test database connection - using text() for SQLAlchemy 2.0
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"
    
    return HealthResponse(
        status="healthy" if db_status == "healthy" else "unhealthy",
        version=settings.app_version,
        database=db_status
    )

@app.post("/api/animal", response_model=AnimalPictureResponse)
async def fetch_animal_picture(
    animal_request: AnimalPictureRequest,
    db: Session = Depends(get_db)
):
    """
    Fetch and store a random animal picture
    """
    request_count.labels(method='POST', endpoint='/api/animal').inc()
    
    try:
        picture = AnimalService.fetch_and_store_picture(animal_request, db)
        return picture
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching picture: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch picture")

@app.get("/api/animal/latest", response_model=AnimalPictureResponse)
async def get_latest_picture(db: Session = Depends(get_db)):
    """
    Get the most recently stored animal picture
    """
    request_count.labels(method='GET', endpoint='/api/animal/latest').inc()
    
    try:
        picture = AnimalService.get_latest_picture(db)
        return picture
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error retrieving picture: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve picture")

@app.get("/api/animal/latest/image")
async def get_latest_picture_image(db: Session = Depends(get_db)):
    """
    Get the actual image data of the latest picture
    """
    try:
        picture = AnimalService.get_latest_picture(db)
        return StreamingResponse(
            io.BytesIO(picture.image_data),
            media_type="image/jpeg"
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error retrieving image: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve image")

@app.get("/api/animal/{picture_id}/image")
async def get_picture_image(picture_id: int, db: Session = Depends(get_db)):
    """
    Get the actual image data by picture ID
    """
    try:
        picture = AnimalService.get_picture_by_id(picture_id, db)
        return StreamingResponse(
            io.BytesIO(picture.image_data),
            media_type="image/jpeg"
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error retrieving image: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve image")

@app.get("/metrics")
async def metrics():
    """
    Prometheus metrics endpoint
    """
    return Response(content=generate_latest(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
