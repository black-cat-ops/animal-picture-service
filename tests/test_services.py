import pytest
from app.services import AnimalService
from app.schemas import AnimalPictureRequest

def test_fetch_and_store_picture(db_session, mocker):
    """Test the service layer for fetching and storing pictures"""
    # Mock requests
    mock_response = mocker.Mock()
    mock_response.content = b"fake_image_data"
    mock_response.raise_for_status = mocker.Mock()
    mocker.patch('requests.get', return_value=mock_response)
    
    request = AnimalPictureRequest(
        animal_type="dog",
        width=300,
        height=300
    )
    
    picture = AnimalService.fetch_and_store_picture(request, db_session)
    assert picture.animal_type == "dog"
    assert picture.width == 300
    assert picture.height == 300
    assert picture.image_data == b"fake_image_data"

def test_get_latest_picture_empty_db(db_session):
    """Test getting latest picture from empty database"""
    with pytest.raises(ValueError, match="No pictures found"):
        AnimalService.get_latest_picture(db_session)

def test_invalid_animal_type_service(db_session):
    """Test invalid animal type at service layer"""
    request = AnimalPictureRequest(
        animal_type="invalid",
        width=400,
        height=400
    )
    
    with pytest.raises(ValueError, match="Invalid animal type"):
        AnimalService.fetch_and_store_picture(request, db_session)
