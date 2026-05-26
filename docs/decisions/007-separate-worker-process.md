# 007 - Separate Worker Process

## Status

Accepted

---

## Context

Transcription is a long-running and compute-heavy workload.

The API should remain responsive while transcription jobs are processed asynchronously in the background.

Running transcription directly inside the API process would create several operational and architectural problems:

- Long-running requests
- API blocking during transcription
- Poor scalability
- Difficult retry handling
- Increased deployment coupling
- Higher failure impact radius
- Reduced operational visibility

Whisper transcription workloads are especially unsuitable for synchronous request/response execution because:

- Model loading is expensive
- Audio processing time varies by file size
- CPU and memory usage are high
- Worker concurrency requirements differ from API concurrency requirements

The project also aims to mirror real production cloud architectures where APIs and background workers are deployed independently.

---

## Decision

Transcription processing will run in a completely separate worker service from the backend API.

The architecture will use:

```text
Frontend
→ Backend API
→ Queue / Job Discovery
→ Worker Service
→ Transcript Storage
```

The backend API will:

- Create jobs
- Validate uploads
- Store job metadata
- Expose job status endpoints
- Orchestrate workflow state

The worker service will:

- Discover queued/uploaded jobs
- Process transcription tasks
- Persist transcript outputs
- Update job lifecycle state
- Handle processing failures

During local development, the worker communicates with the backend using HTTP and shared local filesystem storage.

In AWS environments, this pattern will evolve into:

- SQS-based job delivery
- ECS/Fargate worker tasks
- S3 object storage
- DynamoDB job persistence

---

## Consequences

### Positive

- API responsiveness remains high
- Transcription workloads become independently scalable
- Worker failures are isolated from the API
- Retry handling becomes simpler
- Operational responsibilities are clearly separated
- Architecture maps cleanly to AWS ECS/SQS patterns
- Easier future migration to distributed infrastructure
- Easier observability and monitoring
- Easier future horizontal scaling

### Negative

- Additional service complexity
- Requires inter-service communication
- Requires lifecycle coordination
- More moving parts during local development
- Additional deployment configuration later in AWS

---

## Alternatives Considered

### Run Whisper Directly Inside FastAPI

Rejected because:

- Long-running requests would block API workers
- Scaling API and transcription independently would be impossible
- Higher risk of API instability
- Poor operational separation

### Use AWS Lambda For Transcription

Rejected because:

- Whisper models are large
- Cold starts would be significant
- Runtime duration may exceed practical Lambda limits
- Dependency packaging would become difficult
- ECS/Fargate is operationally better suited for ML workloads

### Use Kubernetes Instead Of ECS/Fargate

Rejected because:

- Kubernetes operational overhead is unnecessary for this project
- ECS/Fargate provides sufficient orchestration capability
- Simpler infrastructure improves maintainability and recruiter readability

---

## Implementation Notes

Initial implementation is intentionally local-first:

- Worker runs as a standalone Python process
- Backend and worker communicate over HTTP
- Shared filesystem storage simulates future S3 integration
- Fake transcription used before introducing Whisper

This validates the orchestration model before introducing heavy ML dependencies or AWS infrastructure.

---

## Related Decisions

- 001 - Use SQS
- 002 - Use ECS Fargate
- 003 - Use DynamoDB
- 004 - Use Presigned S3 URLs
- 006 - Avoid Kubernetes v1
