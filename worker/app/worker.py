import time
import logging
from pathlib import Path

from app.config import TRANSCRIPTS_DIR, UPLOADS_DIR

#from fake_transcriber import generate_fake_transcript
from app.whisper_transcriber import transcribe_audio

from app.job_client import (
    get_uploaded_jobs,
    mark_completed,
    mark_failed,
    mark_processing,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)


def process_job(job: dict) -> None:
    job_id = job["job_id"]
    upload_key = job["upload_key"]

    logger.info("Processing job %s", job_id)

    upload_filename = Path(upload_key).name
    upload_path = UPLOADS_DIR / upload_filename

    if not upload_path.exists():
        error_message = f"Uploaded file not found: {upload_path}"
        logger.error(error_message)
        mark_failed(job_id, error_message)
        return

    mark_processing(job_id)

    try:
        transcript = transcribe_audio(upload_path, model_name="tiny")

        TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

        transcript_path = TRANSCRIPTS_DIR / f"{job_id}.txt"
        transcript_path.write_text(transcript, encoding="utf-8")

        transcript_key = f"transcripts/{job_id}.txt"
        mark_completed(job_id, transcript_key)

        logger.info("Completed job %s", job_id)

    except Exception as exc:
        error_message = f"Transcription failed: {exc}"
        logger.exception(error_message)
        mark_failed(job_id, error_message)


def run_once() -> None:
    jobs = get_uploaded_jobs()

    if not jobs:
        logger.info("No uploaded jobs found")
        return

    for job in jobs:
        process_job(job)


def run_forever(poll_interval_seconds: int = 5) -> None:
    logger.info("Worker started")

    while True:
        run_once()
        time.sleep(poll_interval_seconds)


if __name__ == "__main__":
    run_forever()