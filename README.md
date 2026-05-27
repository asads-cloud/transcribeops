# TranscribeOps

A production-style AWS transcription platform built to demonstrate cloud, platform, and DevOps engineering skills.

## Goal

Users upload an audio file, the system queues a transcription job, a Dockerised worker processes it, and the transcript is displayed in the browser.

## Target Architecture

User → Frontend → FastAPI Backend → S3 Upload → DynamoDB Job Record → SQS Queue → Worker → Transcript Storage

## Tech Stack

- Python
- FastAPI
- Docker
- Docker Compose
- PowerShell
- AWS CLI
- Terraform
- GitHub Actions
- AWS S3
- AWS SQS
- AWS DynamoDB
- AWS ECS/Fargate

## Project Status

Phase 8: PowerShell local automation

## Repository Structure

```text
backend/
worker/
frontend/
infra/
scripts/
docs/
.github/
```

## Build Phases

See docs/build-plan.md.

## Architecture

See docs/architecture.md.

---

## Local Development

Start the full stack locally:

```powershell
docker compose up --build
```

Frontend:

```text
http://127.0.0.1:5173
```

Backend API:

```text
http://127.0.0.1:8000/docs
```