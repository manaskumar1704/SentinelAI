from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "name": "SentinelAI API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
    }

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "sentinelai-backend"}
