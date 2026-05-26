# 008 - Use Whisper for Local Transcription

## Status

Accepted

## Context

The platform requires real speech-to-text transcription capability before containerisation and AWS deployment work can begin.

A production-like worker implementation is needed to validate:

- ML dependency handling
- Audio decoding requirements
- Long-running processing behaviour
- Real transcript generation
- Failure handling for corrupt media
- Runtime performance characteristics

The system already supports asynchronous worker orchestration locally using a fake transcription implementation.

The next step is replacing the fake implementation with a real transcription engine while preserving the worker architecture.

## Decision

Use OpenAI Whisper for local transcription.

Initial implementation uses:

- Whisper `tiny` model
- CPU inference
- Local filesystem storage
- ffmpeg for audio decoding

Whisper execution is isolated inside the worker service.

## Consequences

### Positive

- Real speech-to-text capability demonstrated
- Worker architecture validated under realistic workload
- Runtime dependencies identified before Dockerisation
- Audio decoding behaviour validated early
- Production architecture becomes substantially more credible

### Negative

- Local CPU usage increases significantly
- First model load/download introduces startup latency
- ffmpeg becomes a required system dependency
- Processing time increases versus fake transcription

## Alternatives Considered

### Cloud transcription APIs

Rejected because:

- Less educational value
- Reduced infrastructure ownership
- Less impressive recruiter-facing architecture
- Higher ongoing cost

### GPU acceleration

Deferred because:

- Unnecessary complexity for early local development
- CPU inference sufficient for short test files

### Larger Whisper models

Deferred because:

- Higher resource requirements
- Slower local iteration
- `tiny` sufficient for architecture validation