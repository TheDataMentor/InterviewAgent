import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_read_main():
    """Test main endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    
def test_add_application():
    """Test adding application endpoint"""
    response = client.post(
        "/applications/",
        json={
            "company": "TestCorp",
            "position": "Data Scientist",
            "priority": 2
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "application_id" in data
    
def test_get_applications():
    """Test getting applications endpoint"""
    response = client.get("/applications/")
    assert response.status_code == 200
    data = response.json()
    assert "applications" in data
    assert "stats" in data
    
def test_analyze_job():
    """Test job analysis endpoint"""
    response = client.post(
        "/analyze-job/",
        json={"job_description": "Sample job description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "analysis" in data
    
def test_optimize_resume():
    """Test resume optimization endpoint"""
    response = client.post(
        "/optimize-resume/",
        json={
            "resume": "Sample resume",
            "job_requirements": "Sample requirements"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "optimized_resume" in data
    
def test_error_handling():
    """Test error handling"""
    response = client.post(
        "/applications/",
        json={}  # Invalid data
    )
    assert response.status_code == 422  # Validation error 