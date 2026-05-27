# 009 - Separate Worker Container

## Status

Accepted

## Context

The transcription worker performs long-running CPU-intensive processing using Whisper and ffmpeg.

The backend API must remain responsive and lightweight while transcription jobs execute asynchronously.

The system also needs to mirror the future AWS ECS/Fargate production architecture locally.

## Decision

The backend API and transcription worker are implemented as separate Docker containers orchestrated through Docker Compose.

Both services communicate over HTTP while sharing mounted local filesystem storage during local development.

## Consequences

### Positive

- Preserves clear service boundaries
- Mirrors future distributed cloud architecture
- Allows independent scaling of API and worker
- Simplifies future ECS migration
- Prevents transcription workloads from blocking API responsiveness
- Improves operational clarity and logging separation

### Negative

- Introduces inter-container networking complexity
- Requires shared storage coordination
- Slightly increases local development complexity