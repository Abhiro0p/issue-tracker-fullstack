import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_issues():
    response = client.get("/issues/")
    assert response.status_code == 200
    data = response.json()
    assert "issues" in data
    assert "pagination" in data
    assert "filters" in data

def test_create_issue():
    issue_data = {
        "title": "Test Issue",
        "description": "This is a test issue",
        "status": "open",
        "priority": "medium"
    }
    response = client.post("/issues/", json=issue_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Issue"
    assert "id" in data

def test_get_nonexistent_issue():
    response = client.get("/issues/nonexistent")
    assert response.status_code == 404
