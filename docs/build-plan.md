# Build Plan

## Phase 0 - Project Setup

Create the repository foundation before writing serious code.

### Deliverables

- GitHub repository
- README skeleton
- Basic folder structure
- Initial docs
- PowerShell script placeholders
- Initial commit pushed
- GitHub issues or project board created

### Done Criteria

- Repo exists locally and on GitHub
- Initial commit is pushed
- README explains the project clearly
- Folder structure is clean
- Setup scripts exist

---

# Phase 1 - Define System Contract

Define the architecture, data model, job lifecycle, storage contracts, queue schema, and API contract before implementation begins.

## Deliverables

- Job lifecycle documentation
- Job status definitions
- API endpoint contract
- S3 object path conventions
- SQS message schema
- DynamoDB item structure
- Ownership boundary documentation
- System architecture documentation

## Done Criteria

- Job lifecycle is clearly documented
- Status transitions are defined
- Backend responsibilities are documented
- Worker responsibilities are documented
- S3 object layout is documented
- SQS message format is documented
- DynamoDB schema is documented
- API routes are defined
- Architecture document can fully explain system behaviour before implementation

## Outputs

```text
docs/architecture.md
```
## Key Decisions

- DynamoDB is the source of truth for job state
- SQS decouples API and transcription processing
- S3 stores audio and transcript objects only
- Backend owns orchestration and validation
- Worker owns transcription execution
- API-first design before implementation

---

# Phase 2 - Local Backend MVP

Built the first working backend service locally before introducing AWS, workers, or frontend components.

## Deliverables

- FastAPI backend application
- In-memory job persistence
- Health endpoint
- Job creation endpoint
- Job retrieval endpoint
- Pydantic job models
- Automated pytest coverage
- Swagger/OpenAPI documentation
- Local development workflow

## Done Criteria

- FastAPI server starts locally
- `/health` returns HTTP 200
- `/jobs` creates a new job
- `/jobs/{job_id}` returns an existing job
- Invalid job IDs return HTTP 404
- Job status defaults to `created`
- UUID job IDs are generated correctly
- Tests pass successfully
- OpenAPI docs load successfully

## Outputs

```text
backend/app/main.py
backend/app/routes.py
backend/app/models.py
backend/app/job_store.py
backend/app/config.py
backend/tests/test_routes.py
backend/requirements.txt
```

## Key Decisions

- FastAPI selected for lightweight API development
- Pydantic used for strict schema validation
- In-memory persistence used before introducing databases
- UUIDs used as public job identifiers
- API contract implemented before worker development
- Local-first development before AWS integration
- Automated tests introduced immediately alongside implementation

---

# Phase 3 - Local File Upload Simulation

Introduce local filesystem uploads before implementing cloud object storage.

This phase simulates the future S3 upload pipeline while keeping the system entirely local and easy to debug.

## Deliverables

- Local filesystem storage directories
- File upload endpoint
- Audio file validation
- Upload size validation
- Local upload persistence
- Job metadata updates
- Job lifecycle transition handling
- Expanded automated test coverage

## Done Criteria

- `POST /jobs/{job_id}/upload-local` accepts multipart uploads
- `.mp3`, `.wav`, and `.m4a` files are accepted
- Invalid file extensions return HTTP 400
- Files larger than 5MB return HTTP 400
- Uploaded files are stored locally
- Upload directories are auto-created
- Job status transitions from `created` to `uploaded`
- File size metadata is stored correctly
- Local upload path metadata is stored correctly
- Tests pass successfully

## Outputs

```text
local_storage/uploads/
local_storage/transcripts/

backend/app/config.py
backend/app/models.py
backend/app/job_store.py
backend/app/routes.py
backend/tests/test_routes.py
backend/requirements.txt
```

## Key Decisions

- Local filesystem storage introduced before S3 integration
- Upload validation implemented early to mirror production behaviour
- UUID-based filenames retained for future S3 compatibility
- Local upload paths stored in job metadata for worker access
- File size limits added to reduce abuse risk
- Upload lifecycle simulated locally before queue integration
- API contract expanded incrementally without introducing infrastructure dependencies

---

# Phase 4 - Local Worker Without Whisper

Introduce asynchronous job processing before integrating real ML transcription.

This phase establishes the worker architecture pattern locally using a fake transcription implementation.

The backend and worker now operate as separate processes communicating over HTTP while sharing local filesystem storage.

---

# Deliverables

- Separate local worker service
- Backend worker-support endpoints
- Job polling logic
- Job processing lifecycle handling
- Fake transcript generation
- Local transcript persistence
- Worker logging
- Failure handling for missing uploads
- Local asynchronous processing simulation

---

# Done Criteria

- Worker runs independently from backend
- Worker discovers uploaded jobs successfully
- Worker marks jobs as processing
- Worker creates transcript files locally
- Worker marks jobs as completed
- Missing uploaded files mark jobs as failed
- Transcript files appear in `local_storage/transcripts/`
- Backend and worker communicate successfully via HTTP
- End-to-end local processing flow works correctly

---

# Outputs

## Worker

```text
worker/app/config.py
worker/app/fake_transcriber.py
worker/app/job_client.py
worker/app/worker.py
worker/requirements.txt
```

## Backend Updates

```text
backend/app/routes.py
backend/app/job_store.py
backend/app/models.py
```

## Local Storage

```text
local_storage/transcripts/
```

---

# Key Decisions

- Worker implemented as a completely separate process from the API
- HTTP used between worker and backend to mirror future distributed architecture
- Fake transcription introduced before Whisper integration to validate orchestration first
- Shared filesystem storage used temporarily before S3 integration
- Logging introduced early for operational visibility
- Failure handling implemented before real ML processing

---

# Processing Lifecycle

```text
uploaded
processing
completed
failed
```

---

# Phase 5 - Real Whisper Locally

Replace fake transcript generation with real ML-powered transcription using OpenAI Whisper.

This phase preserves the existing asynchronous worker architecture while introducing real audio decoding and transcription processing.

The system now performs actual speech-to-text transcription locally using the Whisper `tiny` model.

---

# Deliverables

- Whisper transcription integration
- Local Whisper model loading
- Real audio transcription
- Transcription duration logging
- Corrupt audio failure handling
- Transcript text persistence
- Worker integration with Whisper
- Local ffmpeg dependency installation

---

# Done Criteria

- Worker successfully loads Whisper model
- `.mp3` audio files transcribe successfully
- `.wav` audio files transcribe successfully
- Transcript files contain real transcription output
- Corrupt or invalid audio files fail gracefully
- Failed jobs store `error_message`
- Worker logs transcription duration
- Existing job lifecycle remains functional
- Transcript retrieval endpoint returns real transcript text

---

# Outputs

## Worker

```text
worker/app/whisper_transcriber.py
worker/app/worker.py
worker/requirements.txt
```

## Local Runtime Dependencies

```text
ffmpeg
openai-whisper
```

---

# Key Decisions

- Whisper integrated only after validating worker orchestration architecture
- `tiny` model selected first to minimise local CPU and memory requirements
- CPU-based inference retained initially for local simplicity
- Shared filesystem storage retained temporarily before S3 integration
- Whisper model loading abstracted into dedicated module
- Real ML processing introduced before Dockerisation to validate runtime dependencies locally
- ffmpeg introduced as explicit system dependency for audio decoding compatibility

---

# Processing Lifecycle

```text
uploaded
processing
completed
failed
```

---

# Runtime Behaviour

```text
Audio Upload
→ Worker Polling
→ Whisper Model Load
→ Audio Decode via ffmpeg
→ Transcription
→ Transcript File Write
→ Job Completion
```

---

# Phase 6 - Dockerise Backend and Worker

Run the backend and transcription worker as isolated containerised services using Docker and Docker Compose.

This phase transitions the platform from local Python processes into reproducible containerised infrastructure that mirrors the future ECS/Fargate deployment architecture.

The backend and worker now run independently inside containers while sharing mounted local storage for uploads and transcripts.

---

## Deliverables

- Backend Dockerfile
- Worker Dockerfile
- Docker Compose orchestration
- Shared mounted storage volume
- Container networking
- Environment variable configuration
- ffmpeg installation inside worker container
- Whisper execution inside Docker
- Containerised end-to-end transcription flow
- Docker logging visibility

---

## Done Criteria

- `docker compose up --build` starts successfully
- Backend container starts correctly
- Worker container starts correctly
- FastAPI accessible on port `8000`
- Health endpoint returns HTTP `200`
- Audio uploads succeed through containerised backend
- Worker container detects uploaded jobs
- Worker container accesses shared uploads directory
- Whisper model loads successfully inside container
- Transcript files are written successfully
- Job lifecycle completes successfully
- Transcript endpoint returns completed transcript
- Logs visible through Docker Compose logging

---

## Outputs

### Docker Infrastructure

- `backend/Dockerfile`
- `worker/Dockerfile`
- `docker-compose.yml`

### Backend Updates

- `backend/app/config.py`
- `backend/requirements.txt`

### Worker Updates

- `worker/app/config.py`
- `worker/app/worker.py`
- `worker/requirements.txt`

---

## Key Decisions

- Docker introduced before AWS deployment to validate runtime reproducibility
- Backend and worker containerised separately to preserve service boundaries
- Docker Compose used for local orchestration before ECS adoption
- Shared bind-mounted local storage retained temporarily before S3 migration
- `ffmpeg` installed directly inside worker container for audio decoding compatibility
- Environment variables introduced for runtime configuration flexibility
- Container networking mirrors future distributed cloud deployment patterns
- Whisper execution validated inside container before AWS infrastructure integration

---

## Runtime Behaviour

```text
User Upload
→ FastAPI Container
→ Shared Mounted Storage
→ Worker Container Polling
→ Whisper Transcription
→ Transcript File Write
→ Job Completion
```

## Container Architecture

```text
Docker Compose
├── backend
│   └── FastAPI API
│
├── worker
│   └── Whisper transcription worker
│
└── shared local_storage volume
```

---

# Phase 7 - Basic Frontend

## Overview

Create the first recruiter-facing user interface for the transcription platform.

This phase introduces a browser-based workflow allowing users to:

- Upload audio files
- Monitor asynchronous transcription progress
- Read completed transcripts

The frontend communicates with the existing FastAPI backend while preserving the asynchronous worker architecture introduced in previous phases.

The system now behaves as a complete local full-stack application.

---

# Deliverables

## Frontend Application

- React frontend application
- Browser-based upload workflow
- Frontend routing
- Job polling interface
- Transcript display UI
- Architecture overview page
- GitHub repository linking
- Frontend API integration

## Containerisation

- Frontend Docker container
- Full-stack Docker Compose orchestration

## Workflow

- Browser-based end-to-end workflow

---

# Done Criteria

- Frontend loads successfully in browser
- Upload page accepts audio file uploads
- Frontend creates jobs through backend API
- Frontend uploads audio files successfully
- Job status updates automatically through polling
- Completed transcripts display in browser
- Failed jobs display visible error messages
- Architecture page explains local system behaviour
- Frontend container runs successfully through Docker Compose
- No Postman usage required for happy-path operation
- End-to-end browser workflow functions correctly

---

# Outputs

## Frontend

```text
frontend/
├── Dockerfile
├── package.json
├── vite.config.js
├── index.html
│
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── api.js
    ├── style.css
    │
    └── pages/
        ├── Home.jsx
        ├── Upload.jsx
        ├── JobStatus.jsx
        └── Architecture.jsx
```

---

## Backend Updates

```text
backend/
└── app/
    ├── main.py
    └── routes.py

backend/requirements.txt
```

---

## Docker Updates

```text
docker-compose.yml
```

---

## Docker Ignore Files

```text
backend/.dockerignore
worker/.dockerignore
frontend/.dockerignore
```

---

# Key Decisions

- React selected for lightweight recruiter-facing frontend development
- Vite selected for fast local frontend iteration
- Frontend implemented only after backend and worker architecture stabilised
- Polling selected initially instead of WebSockets to minimise complexity
- Frontend containerised separately to preserve service boundaries
- Browser-based workflow introduced before AWS deployment to validate full-stack behaviour locally
- Simple CSS retained initially to prioritise architecture and workflow clarity
- Frontend API abstraction introduced before cloud infrastructure integration
- CORS enabled explicitly to support distributed frontend/backend architecture

---

# Runtime Behaviour

```text
Browser UI
    ↓
React Frontend
    ↓
FastAPI Backend
    ↓
Worker Polling
    ↓
Whisper Transcription
    ↓
Transcript Retrieval
    ↓
Frontend Transcript Display
```

---

# Frontend Architecture

```text
Docker Compose
├── frontend
│   └── React/Vite application
│
├── backend
│   └── FastAPI API
│
├── worker
│   └── Whisper transcription worker
│
└── shared local_storage volume
```

---

# Phase 8 - PowerShell Local Automation

## Overview

Improve the local developer experience by introducing repeatable PowerShell automation workflows.

This phase transforms the project from a manually operated local application into a reproducible developer platform with one-command setup, testing, image builds, and cleanup workflows.

The repository now provides a significantly smoother onboarding experience while demonstrating Windows-focused platform engineering and automation skills.

---

## Deliverables

### PowerShell Automation
- Local environment setup script
- Automated Docker image build script
- Automated test execution script
- Local cleanup/reset script
- Docker validation logic
- Local storage bootstrap logic
- `.env` bootstrap workflow
- Exit code handling

### Developer Workflow Improvements
- One-command local startup
- One-command cleanup
- One-command testing
- Reduced onboarding friction
- Repeatable local workflows

---

## Done Criteria

- `./scripts/setup-local.ps1` starts the full platform
- Docker installation validation works correctly
- `.env` auto-creation works correctly
- Local storage folders auto-create successfully
- `docker compose up --build` launches successfully through script
- `./scripts/build-images.ps1` builds all images successfully
- `./scripts/run-tests.ps1` executes backend tests successfully
- Worker tests execute conditionally when present
- `./scripts/clean-local.ps1` resets local environment successfully
- Frontend workflow still operates correctly after cleanup/setup cycle
- Full local platform remains operational after automation introduction

---

## Outputs

### PowerShell Scripts
- `scripts/setup-local.ps1`
- `scripts/run-tests.ps1`
- `scripts/build-images.ps1`
- `scripts/clean-local.ps1`

### Documentation Updates
- `README.md`
- `docs/build-plan.md`

### ADRs
- `docs/decisions/010-use-powershell-local-automation.md`

---

## Key Decisions

- PowerShell selected to prioritise Windows-native developer workflows
- Automation introduced before AWS deployment to reduce operational friction early
- Docker Compose retained as the orchestration layer beneath automation scripts
- Environment bootstrapping automated to reduce onboarding errors
- Cleanup workflow added to simplify repeated testing and debugging cycles
- Test automation introduced before CI/CD pipeline implementation
- Scripts designed to mirror future operational workflows used in deployment automation
- Exit-code validation added to improve reliability and debugging visibility

---

## Runtime Behaviour

```text
Developer
    ↓
PowerShell Automation
    ↓
Docker Compose
    ↓
Frontend + Backend + Worker Containers
    ↓
Shared Local Storage
```

---

## Automation Workflow

### setup-local.ps1

```text
setup-local.ps1
├── Validate Docker
├── Create .env if missing
├── Create local storage directories
└── Start Docker Compose
```

### run-tests.ps1

```text
run-tests.ps1
├── Build backend image
├── Build worker image
├── Run backend pytest suite
└── Conditionally run worker tests
```

### build-images.ps1

```text
build-images.ps1
├── Build backend image
├── Build worker image
└── Build frontend image
```

### clean-local.ps1

```text
clean-local.ps1
├── Stop containers
├── Remove orphan containers
├── Clear local storage
└── Recreate local directories
```

---

# Phase 9 - AWS Mode Abstraction

Prepare the application for future AWS infrastructure integration without deploying real AWS resources yet.

## Deliverables

- Environment-based infrastructure mode selection
- Storage service abstraction
- Queue service abstraction
- Job repository abstraction
- Local implementation classes
- AWS placeholder implementation classes
- Service factory pattern
- Refactored backend route dependencies

## Done Criteria

- Application runs fully in local mode
- Routes depend on service interfaces
- Local implementation details are abstracted
- Environment variables determine implementations
- AWS-ready boundaries exist
- Local developer workflow remains unchanged

## Outputs

backend/app/services/
backend/app/services/storage.py
backend/app/services/queue.py
backend/app/services/repositories.py
backend/app/services/factory.py

docs/decisions/011-introduce-service-abstractions.md

.env.example

## Key Decisions

- Application logic must not directly depend on infrastructure implementations
- AWS integration will be introduced through implementation swapping
- Local development experience must remain first-class
- Service factory pattern used for implementation selection

## Why This Matters

This phase establishes clean architecture boundaries before introducing real AWS infrastructure.

It prevents AWS-specific logic from being scattered throughout the application and significantly reduces future migration complexity.

---

## Phase 10 - Terraform S3/SQS/DynamoDB

Create the first AWS infrastructure resources using Terraform.

### Deliverables

- Terraform AWS provider setup
- S3 uploads bucket
- S3 transcripts bucket
- SQS transcription queue
- SQS dead-letter queue
- DynamoDB jobs table
- Least-privilege IAM policies
- Terraform outputs
- AWS CLI verification

### Done Criteria

- terraform init succeeds
- terraform validate succeeds
- terraform plan succeeds
- terraform apply succeeds
- S3 buckets exist
- SQS queues exist
- DynamoDB table exists
- IAM policies exist
- AWS CLI verification succeeds