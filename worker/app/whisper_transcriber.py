import logging
import time
from pathlib import Path

import whisper

logger = logging.getLogger(__name__)

_model = None


def get_model(model_name: str = "tiny"):
    global _model

    if _model is None:
        logger.info("Loading Whisper model: %s", model_name)
        _model = whisper.load_model(model_name)

    return _model


def transcribe_audio(audio_path: Path, model_name: str = "tiny") -> str:
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    start_time = time.perf_counter()

    logger.info("Starting transcription for %s", audio_path)

    model = get_model(model_name)
    result = model.transcribe(str(audio_path), fp16=False)

    duration_seconds = time.perf_counter() - start_time

    logger.info(
        "Completed transcription for %s in %.2f seconds",
        audio_path,
        duration_seconds,
    )

    transcript = result.get("text", "").strip()

    if not transcript:
        raise ValueError("Whisper returned an empty transcript")

    return transcript