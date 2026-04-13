import pytest
from fastapi.testclient import TestClient
from main import socket_app as app  # socket_app is ASGIApp

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Errand.NG Backend v2" in response.json()["message"]

def test_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_create_errand():
    errand_data = {
        "title": "Test Market Run",
        "description": "Buy groceries",
        "category": "delivery",
        "pickup_lat": 5.031,
        "pickup_lng": 7.92,
        "dropoff_lat": 5.037,
        "dropoff_lng": 7.925,
        "price": 5000
    }
    response = client.post("/errands/", json=errand_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Market Run"

if __name__ == "__main__":
    pytest.main(["-v"])
