def test_home_endpoint(client):
    """Test the home endpoint returns OK status."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
