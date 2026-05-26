from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    created = "created"
    uploading = "uploading"
    uploaded = "uploaded"
    queued = "queued"
    processing = "processing"
    completed = "completed"
    failed = "failed"
    expired = "expired"


class Job(BaseModel):
    job_id: str
    status: JobStatus = JobStatus.created
    upload_key: str
    transcript_key: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None
    error_message: Optional[str] = None
    file_size_bytes: int = 0
    model: str = "tiny"
    local_upload_path: str | None = None
