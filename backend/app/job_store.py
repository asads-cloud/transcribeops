from typing import Dict, Optional
from uuid import uuid4

from datetime import datetime, timezone
from app.models import Job


_jobs: Dict[str, Job] = {}


def create_job() -> Job:
    job_id = str(uuid4())

    job = Job(
        job_id=job_id,
        upload_key=f"uploads/{job_id}/audio.mp3",
    )

    _jobs[job_id] = job
    return job


def get_job(job_id: str) -> Optional[Job]:
    return _jobs.get(job_id)


def clear_jobs() -> None:
    _jobs.clear()


def update_job(job_id: str, updates: dict):
    job = get_job(job_id)

    for key, value in updates.items():
        setattr(job, key, value)

    job.updated_at = datetime.now(timezone.utc)
    return job