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