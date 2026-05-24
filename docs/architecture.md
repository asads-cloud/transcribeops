# Architecture

TranscribeOps is a cloud transcription platform designed around asynchronous processing.

## High-Level Flow

1. User uploads an audio file.
2. Backend creates a job record.
3. Backend generates a presigned S3 upload URL.
4. User uploads audio to S3.
5. Backend queues a transcription job in SQS.
6. Worker processes the audio file.
7. Worker stores the transcript.
8. Frontend polls the backend for status and transcript.

## Core AWS Services

- S3 for audio and transcript storage
- DynamoDB for job metadata
- SQS for job queueing
- ECS/Fargate for backend and worker containers
- ALB for backend ingress
- CloudFront/S3 for frontend hosting