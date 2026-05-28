from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from app.config import (
    ALLOWED_AUDIO_EXTENSIONS,
    MAX_UPLOAD_SIZE_BYTES,
    TRANSCRIPTS_DIR,
    UPLOADS_DIR,
)
from app.models import Job, JobStatus
from app.services.factory import (
    get_job_repository,
    get_queue_service,
    get_storage_service,
)


router = APIRouter()

storage_service = get_storage_service()
queue_service = get_queue_service()
job_repository = get_job_repository()


class JobFailureRequest(BaseModel):
    error_message: str


@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@router.post("/jobs", response_model=Job, status_code=201)
def create_transcription_job() -> Job:
    return job_repository.create_job()


@router.get("/jobs", response_model=list[Job])
def list_transcription_jobs(status: JobStatus | None = None) -> list[Job]:
    jobs = job_repository.list_jobs()

    if status is not None:
        jobs = [job for job in jobs if job.status == status]

    return jobs


@router.get("/jobs/{job_id}", response_model=Job)
def get_transcription_job(job_id: str) -> Job:
    job = job_repository.get_job(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return job


@router.post("/jobs/{job_id}/upload-local")
async def upload_local_file(job_id: str, file: UploadFile = File(...)):
    job = job_repository.get_job(job_id)

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

    upload_key = storage_service.save_upload(
        job_id,
        file.filename,
        contents,
    )

    upload_path = UPLOADS_DIR / f"{job_id}{file_extension}"

    updated_job = job_repository.update_job(
        job_id,
        {
            "status": JobStatus.uploaded,
            "file_size_bytes": len(contents),
            "local_upload_path": str(upload_path),
            "upload_key": upload_key,
            "transcript_key": f"transcripts/{job_id}.txt",
        },
    )

    queue_service.enqueue_transcription_job(
        updated_job.job_id,
        updated_job.upload_key,
        updated_job.transcript_key,
        "tiny",
    )

    return updated_job


@router.post("/jobs/{job_id}/processing", response_model=Job)
def mark_job_processing(job_id: str) -> Job:
    job = job_repository.get_job(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return job_repository.update_job(
        job_id,
        {
            "status": JobStatus.processing,
        },
    )


@router.post("/jobs/{job_id}/complete-local", response_model=Job)
def mark_job_completed_local(job_id: str) -> Job:
    job = job_repository.get_job(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return job_repository.update_job(
        job_id,
        {
            "status": JobStatus.completed,
            "transcript_key": f"transcripts/{job_id}.txt",
            "local_transcript_path": str(TRANSCRIPTS_DIR / f"{job_id}.txt"),
        },
    )


@router.post("/jobs/{job_id}/fail", response_model=Job)
def mark_job_failed(job_id: str, request: JobFailureRequest) -> Job:
    job = job_repository.get_job(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return job_repository.update_job(
        job_id,
        {
            "status": JobStatus.failed,
            "error_message": request.error_message,
        },
    )


@router.get("/jobs/{job_id}/transcript", response_class=PlainTextResponse)
def get_job_transcript(job_id: str) -> str:
    job = job_repository.get_job(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.status != JobStatus.completed:
        raise HTTPException(status_code=400, detail="Job is not completed yet")

    if job.transcript_key is None:
        raise HTTPException(status_code=404, detail="Transcript key not found")

    try:
        return storage_service.get_transcript(job.transcript_key)

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Transcript file not found")