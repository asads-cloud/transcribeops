# RUNBOOK

# Purpose

This runbook documents the local operational workflow for TranscribeOps.

It explains:

- How to start the platform
- How to stop the platform
- How to inspect logs
- How to validate services
- How to troubleshoot common issues
- How the local runtime behaves

This runbook will expand further during AWS deployment phases.

---

# Local Platform Architecture

```text
Browser
→ React Frontend
→ FastAPI Backend
→ Whisper Worker
→ Local Storage
```

Docker Compose orchestrates all local services.

---

# Local Development

## Start Full Platform

From the repository root:

```powershell
docker compose up --build
```

Expected services:

```text
transcribeops-frontend
transcribeops-backend
transcribeops-worker
```

---

## Stop Full Platform

```powershell
docker compose down
```

---

## Rebuild Containers

```powershell
docker compose up --build
```

---

# Service URLs

## Frontend

```text
http://127.0.0.1:5173
```

---

## Backend API

```text
http://127.0.0.1:8000
```

---

## Swagger/OpenAPI Docs

```text
http://127.0.0.1:8000/docs
```

---

# Container Operations

## View All Logs

```powershell
docker compose logs -f
```

---

## View Backend Logs

```powershell
docker compose logs -f backend
```

---

## View Worker Logs

```powershell
docker compose logs -f worker
```

---

## View Frontend Logs

```powershell
docker compose logs -f frontend
```

---

# Testing the Full Workflow

## Step 1 — Open Frontend

Open:

```text
http://127.0.0.1:5173
```

---

## Step 2 — Upload Audio

Navigate to:

```text
Upload
```

Choose a supported audio file:

```text
.mp3
.wav
.m4a
```

---

## Step 3 — Start Transcription

Click:

```text
Start transcription
```

Expected behaviour:

```text
Frontend creates job
→ File uploads
→ Worker detects uploaded job
→ Worker processes transcription
→ Frontend polls status
→ Transcript appears
```

---

# Health Validation

## Backend Health Check

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

# Local Storage

## Upload Storage

Uploaded audio files are stored under:

```text
local_storage/uploads/
```

---

## Transcript Storage

Generated transcripts are stored under:

```text
local_storage/transcripts/
```

---

# Runtime Behaviour

## Current Local Processing Flow

```text
Browser Upload
→ FastAPI API
→ Local Storage Write
→ Worker Polling
→ Whisper Transcription
→ Transcript File Write
→ Frontend Polling
→ Transcript Display
```

---

# Whisper Runtime Notes

## First Startup Behaviour

The first worker startup may take longer because the Whisper model downloads automatically.

Expected behaviour.

---

## CPU-only Inference

Whisper currently runs on CPU only.

Longer audio files may process slowly.

Expected for local development.

---

# Common Failure Scenarios

## Frontend Cannot Reach Backend

Symptoms:

```text
Failed to fetch
CORS errors
Frontend API errors
```

Checks:

```powershell
docker compose ps
```

Verify backend container is running.

Verify:

```text
http://127.0.0.1:8000/health
```

returns HTTP 200.

---

## Worker Not Processing Jobs

Symptoms:

```text
Jobs remain in uploaded status
```

Checks:

```powershell
docker compose logs -f worker
```

Verify worker polling messages appear.

---

## Whisper Fails to Transcribe

Symptoms:

```text
Job status becomes failed
```

Possible causes:

- Invalid audio file
- Corrupt upload
- Unsupported encoding
- ffmpeg issue

Inspect worker logs:

```powershell
docker compose logs -f worker
```

---

## Port Already In Use

Symptoms:

```text
Bind errors during docker compose startup
```

Possible conflicting ports:

```text
5173
8000
```

Stop conflicting applications or containers.

---

# Automated Tests

## Backend Tests

From repository root:

```powershell
python -m pytest
```

---

# Planned Future Expansion

This runbook will later include:

- AWS deployment operations
- ECS service debugging
- CloudWatch troubleshooting
- SQS queue inspection
- DynamoDB validation
- IAM troubleshooting
- Terraform operations
- Disaster recovery procedures
- Deployment rollback procedures
- Cost incident handling
- WAF and abuse-response procedures
```