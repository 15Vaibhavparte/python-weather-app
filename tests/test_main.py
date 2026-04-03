from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_weather():
    response = client.get("/weather/London")
    assert response.status_code == 200
    assert "temperature" in response.json()