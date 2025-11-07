def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data

def test_fetch_animal_picture(client, mocker):
    """Test fetching and storing an animal picture"""
    # Mock the external API call
    mock_response = mocker.Mock()
    mock_response.content = b"fake_image_data"
    mock_response.raise_for_status = mocker.Mock()
    mocker.patch('requests.get', return_value=mock_response)
    
    response = client.post(
        "/api/animal",
        json={"animal_type": "cat", "width": 400, "height": 400}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["animal_type"] == "cat"
    assert data["width"] == 400
    assert data["height"] == 400

def test_get_latest_picture_not_found(client):
    """Test getting latest picture when database is empty"""
    response = client.get("/api/animal/latest")
    assert response.status_code == 404

def test_invalid_animal_type(client):
    """Test invalid animal type"""
    response = client.post(
        "/api/animal",
        json={"animal_type": "elephant", "width": 400, "height": 400}
    )
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
