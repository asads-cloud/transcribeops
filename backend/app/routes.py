from app.models import Job, JobStatus

from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File

from app.config import (
    UPLOADS_DIR,
    TRANSCRIPTS_DIR,
    ALLOWED_AUDIO_EXTENSIONS,
    MAX_UPLOAD_SIZE_BYTES,
)
from app.job_store import create_job, get_job, update_job, list_jobs
router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@router.post("/jobs", response_model=Job, status_code=201)
def create_transcription_job() -> Job:
    return create_job()


@router.get("/jobs", response_model=list[Job])
def list_transcription_jobs(status: JobStatus | None = None) -> list[Job]:
    jobs = list_jobs()

    if status is not None:
        jobs = [job for job in jobs if job.status == status]

    return jobs


@router.get("/jobs/{job_id}", response_model=Job)
def get_transcription_job(job_id: str) -> Job:
    job = get_job(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return job


@router.post("/jobs/{job_id}/upload-local")
async def upload_local_file(job_id: str, file: UploadFile = File(...)):
    job = get_job(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Allowed types: mp3, wav, m4a",
        )

    contents = await file.read()

    if len(contents) > MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum upload size is 5MB",
        )

    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

    upload_path = UPLOADS_DIR / f"{job_id}{file_extension}"
    upload_path.write_bytes(contents)

    updated_job = update_job(
        job_id,
        {
            "status": JobStatus.uploaded,
            "file_size_bytes": len(contents),
            "local_upload_path": str(upload_path),
            "upload_key": f"uploads/{job_id}{file_extension}",
        },
    )

    return updated_job


@router.post("/jobs/{job_id}/processing", response_model=Job)
def mark_job_processing(job_id: str) -> Job:
    job = get_job(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return update_job(
        job_id,
        {
            "status": JobStatus.processing,
        },
    )


@router.post("/jobs/{job_id}/complete-local", response_model=Job)
def mark_job_completed_local(job_id: str) -> Job:
    job = get_job(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return update_job(
        job_id,
        {
            "status": JobStatus.completed,
            "transcript_key": f"transcripts/{job_id}.txt",
            "local_transcript_path": str(TRANSCRIPTS_DIR / f"{job_id}.txt"),
        },
    )


@router.post("/jobs/{job_id}/fail", response_model=Job)
def mark_job_failed(job_id: str) -> Job:
    job = get_job(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return update_job(
        job_id,
        {
            "status": JobStatus.failed,
        },
    )