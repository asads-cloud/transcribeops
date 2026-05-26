from pathlib import Path


APP_NAME = "TranscribeOps API"
APP_VERSION = "0.1.0"

BASE_DIR = Path(__file__).resolve().parents[2]

LOCAL_STORAGE_DIR = BASE_DIR / "local_storage"
UPLOADS_DIR = LOCAL_STORAGE_DIR / "uploads"
TRANSCRIPTS_DIR = LOCAL_STORAGE_DIR / "transcripts"

ALLOWED_AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a"}
MAX_UPLOAD_SIZE_BYTES = 5 * 1024 * 1024