# TranscribeOps

Production-style cloud transcription platform built to demonstrate platform engineering, DevOps, and AWS infrastructure skills.

Users upload audio files through a browser UI, transcription jobs are processed asynchronously by Dockerised Whisper workers, and completed transcripts are returned through the frontend.

---

## Current Status

Phase 8 — PowerShell Local Automation

Current implementation supports:

- React frontend
- FastAPI backend
- Whisper transcription worker
- Docker Compose orchestration
- Local asynchronous job processing
- Automated PowerShell developer workflows

AWS infrastructure deployment begins in later phases.

---

## Planned AWS Architecture

```text
User
→ CloudFront Frontend
→ FastAPI Backend (ALB)
→ S3 Upload Storage
→ DynamoDB Job Metadata
→ SQS Transcription Queue
→ ECS/Fargate Whisper Worker
→ S3 Transcript Storage
```

---

## Tech Stack

### Application

- Python
- FastAPI
- React
- Vite
- OpenAI Whisper

### Platform / DevOps

- Docker
- Docker Compose
- PowerShell
- GitHub Actions
- Terraform
- AWS CLI

### AWS Services

- S3
- SQS
- DynamoDB
- ECS/Fargate
- ALB
- CloudFront
- Route 53
- WAF

---

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

---

## Local Development

### Start Full Platform

```powershell
.\scripts\setup-local.ps1
```

### Run Tests

```powershell
.\scripts\run-tests.ps1
```

### Build Docker Images

```powershell
.\scripts\build-images.ps1
```

### Clean Local Environment

```powershell
.\scripts\clean-local.ps1
```

---

## Local URLs

Frontend:

```text
http://127.0.0.1:5173
```

Backend API:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

## Documentation

| Document | Purpose |
|---|---|
| `docs/build-plan.md` | Incremental implementation roadmap |
| `docs/architecture.md` | System architecture and lifecycle design |
| `RUNBOOK.md` | Operational workflows and troubleshooting |
| `SECURITY.md` | Security strategy and hardening plans |
| `COST.md` | Cost-control and scaling strategy |

---

## Current Local Architecture

```text
Browser
→ React Frontend
→ FastAPI Backend
→ Worker Polling
→ Whisper Transcription
→ Transcript Retrieval
→ Frontend Display
```

---

## Infrastructure Modes

The backend supports environment-based infrastructure abstraction.

Current supported modes:

- local
- aws (prepared, not yet implemented)

Configuration:

```env
STORAGE_MODE=local
QUEUE_MODE=local
DATABASE_MODE=local
```

This architecture allows the application to switch between local and AWS-backed implementations without changing application logic.

---

# 4. Recommended validation

Run:

```powershell
.\scripts\clean-local.ps1
.\scripts\setup-local.ps1
.\scripts\run-tests.ps1
```

Then manually validate:

- upload flow
- worker processing
- transcript retrieval
- frontend polling