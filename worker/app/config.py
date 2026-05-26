from pathlib import Path

BACKEND_URL = "http://127.0.0.1:8000"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOCAL_STORAGE_DIR = PROJECT_ROOT / "local_storage"
UPLOADS_DIR = LOCAL_STORAGE_DIR / "uploads"
TRANSCRIPTS_DIR = LOCAL_STORAGE_DIR / "transcripts"