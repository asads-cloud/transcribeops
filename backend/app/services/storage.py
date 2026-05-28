from abc import ABC, abstractmethod
from pathlib import Path

from app import config


class StorageService(ABC):
    @abstractmethod
    def save_upload(self, job_id: str, filename: str, content: bytes) -> str:
        pass

    @abstractmethod
    def get_transcript(self, transcript_key: str) -> str:
        pass


class LocalStorageService(StorageService):
    def save_upload(self, job_id: str, filename: str, content: bytes) -> str:
        file_extension = Path(filename).suffix.lower()

        config.UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

        upload_path = config.UPLOADS_DIR / f"{job_id}{file_extension}"
        upload_path.write_bytes(content)

        return f"uploads/{job_id}{file_extension}"

    def get_transcript(self, transcript_key: str) -> str:
        transcript_path = config.LOCAL_STORAGE_DIR / transcript_key

        if not transcript_path.exists():
            raise FileNotFoundError("Transcript not found")

        return transcript_path.read_text(encoding="utf-8")


class S3StorageService(StorageService):
    def save_upload(self, job_id: str, filename: str, content: bytes) -> str:
        raise NotImplementedError("S3 storage is prepared but not implemented yet")

    def get_transcript(self, transcript_key: str) -> str:
        raise NotImplementedError("S3 storage is prepared but not implemented yet")