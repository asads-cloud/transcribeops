from fastapi import APIRouter, HTTPException

from app.job_store import create_job, get_job
from app.models import Job


router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@router.post("/jobs", response_model=Job, status_code=201)
def create_transcription_job() -> Job:
    return create_job()


@router.get("/jobs/{job_id}", response_model=Job)
def get_transcription_job(job_id: str) -> Job:
    job = get_job(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return job