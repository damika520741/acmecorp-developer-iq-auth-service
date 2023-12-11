from fastapi.testclient import TestClient
from fastapi import status
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == dict(
        is_success=True, 
        status_code=status.HTTP_200_OK, 
        message="acmecorp-developer-iq-auth-service",
        data=None
    )