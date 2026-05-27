import requests

from app.config import BACKEND_URL


def get_uploaded_jobs() -> list[dict]:
    response = requests.get(f"{BACKEND_URL}/jobs", params={"status": "uploaded"})
    response.raise_for_status()
    return response.json()


def mark_processing(job_id: str) -> dict:
    response = requests.post(f"{BACKEND_URL}/jobs/{job_id}/processing")
    response.raise_for_status()
    return response.json()


def mark_completed(job_id: str, transcript_key: str) -> dict:
    response = requests.post(
        f"{BACKEND_URL}/jobs/{job_id}/complete-local",
        json={"transcript_key": transcript_key},
    )
    response.raise_for_status()
    return response.json()


def mark_failed(job_id: str, error_message: str) -> dict:
    response = requests.post(
        f"{BACKEND_URL}/jobs/{job_id}/fail",
        json={"error_message": error_message},
    )
    response.raise_for_status()
    return response.json()