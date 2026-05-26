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