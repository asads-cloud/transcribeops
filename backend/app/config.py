import os
from pathlib import Path


APP_NAME = "TranscribeOps API"
APP_VERSION = "0.1.0"

BASE_DIR = Path(__file__).resolve().parents[2]

APP_ENV = os.getenv("APP_ENV", "local")

STORAGE_MODE = os.getenv("STORAGE_MODE", "local")
QUEUE_MODE = os.getenv("QUEUE_MODE", "local")
DATABASE_MODE = os.getenv("DATABASE_MODE", "local")

AWS_REGION = os.getenv("AWS_REGION", "eu-west-2")

UPLOAD_BUCKET = os.getenv("UPLOAD_BUCKET", "")
TRANSCRIPT_BUCKET = os.getenv("TRANSCRIPT_BUCKET", "")
TRANSCRIPTION_QUEUE_URL = os.getenv("TRANSCRIPTION_QUEUE_URL", "")
JOBS_TABLE_NAME = os.getenv("JOBS_TABLE_NAME", "")

LOCAL_STORAGE_DIR = Path(
    os.getenv("LOCAL_STORAGE_DIR", str(BASE_DIR / "local_storage"))
)

UPLOADS_DIR = LOCAL_STORAGE_DIR / "uploads"
TRANSCRIPTS_DIR = LOCAL_STORAGE_DIR / "transcripts"

ALLOWED_AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a"}
MAX_UPLOAD_SIZE_BYTES = 5 * 1024 * 1024