import pytest
from fastapi.testclient import TestClient
import sys, os
import uuid


# Ensure the app module is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app  # Correct import

client = TestClient(app)

@pytest.fixture
def sample_cv():
    unique_email = f"john.doe_{uuid.uuid4().hex}@example.com"
    return {
         "full_name": "John Doe",
         "email": unique_email,
         "phone": "+1234567890",
         "location": "New York",
         "education": [
        {
            "degree": "BSc Computer Science",
            "school": "NYU",
            "year": "2020"
        }
    ],
    "experience": [
        {
            "title": "Developer",
            "company": "TechCorp",
            "duration": "2 years",
            "technologies": ["Python", "FastAPI", "MongoDB"]
        }
    ],
    "skills": ["Python", "FastAPI", "Docker"],
    "languages": ["English", "French"]
    }

def test_create_cv(sample_cv):
    response = client.post("/api/v1/cv/", json=sample_cv)
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == sample_cv["full_name"]
    return data["_id"]

def test_get_all_cvs():
    response = client.get("/api/v1/cv/")
    assert response.status_code in (200, 404)  # 404 if DB empty

def test_crud_flow(sample_cv):
    # Create
    create_resp = client.post("/api/v1/cv/", json=sample_cv)
    assert create_resp.status_code == 200
    cv_id = create_resp.json()["_id"]

    # Read
    get_resp = client.get(f"/api/v1/cv/{cv_id}")
    assert get_resp.status_code == 200

    # Update
    updated_data = sample_cv.copy()
    updated_data["full_name"] = "Jane Doe"
    update_resp = client.put(f"/api/v1/cv/{cv_id}", json=updated_data)
    assert update_resp.status_code == 200
    assert update_resp.json()["full_name"] == "Jane Doe"

    # Delete
    delete_resp = client.delete(f"/api/v1/cv/{cv_id}")
    assert delete_resp.status_code == 200
