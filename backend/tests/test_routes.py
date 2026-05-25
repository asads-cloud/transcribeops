from fastapi.testclient import TestClient

from app.job_store import clear_jobs
from app.main import app


client = TestClient(app)


def setup_function() -> None:
    clear_jobs()


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_job() -> None:
    response = client.post("/jobs")

    data = response.json()

    assert response.status_code == 201
    assert data["status"] == "created"
    assert data["job_id"] is not None
    assert data["model"] == "tiny"


def test_get_existing_job() -> None:
    create_response = client.post("/jobs")
    job_id = create_response.json()["job_id"]

    response = client.get(f"/jobs/{job_id}")

    assert response.status_code == 200
    assert response.json()["job_id"] == job_id


def test_get_unknown_job_returns_404() -> None:
    response = client.get("/jobs/not-a-real-id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"


def test_job_ids_are_unique() -> None:
    first_job = client.post("/jobs").json()
    second_job = client.post("/jobs").json()

    assert first_job["job_id"] != second_job["job_id"]