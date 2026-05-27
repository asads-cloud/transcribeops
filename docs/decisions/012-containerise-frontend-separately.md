# 012 - Containerise Frontend Separately

## Status

Accepted

---

## Context

The platform architecture already separated:

- Backend API service
- Transcription worker service

The new frontend application required deployment consistency alongside the existing Docker-based workflow.

The project also needed to mirror future cloud deployment patterns where frontend and backend services evolve independently.

---

## Decision

Run the frontend as a completely separate Docker container managed through Docker Compose.

The frontend container communicates with the backend through HTTP APIs.

---

## Consequences

### Positive

- Clear service boundaries
- Independent frontend deployment lifecycle
- Better production parity
- Easier future migration to CloudFront hosting
- Cleaner local orchestration
- Improved recruiter-facing architecture clarity

### Negative

- Additional Docker image build
- Additional container startup time
- Additional compose orchestration complexity

---

## Alternatives Considered

### Serve Frontend Through FastAPI

Rejected because:

- Frontend and backend concerns become tightly coupled
- Reduced deployment flexibility
- Less representative of modern frontend hosting patterns
- Harder future migration to CDN hosting

---

### Local Frontend Without Docker

Rejected because:

- Reduced environment consistency
- Reduced deployment reproducibility
- Less realistic infrastructure simulation

---

## Operational Impact

Docker Compose now orchestrates:

```text
frontend
backend
worker
```

This mirrors future production separation between:

```text
CloudFront frontend
ALB backend API
ECS worker services
```

---

## Future Evolution

The frontend container is temporary local infrastructure.

Future AWS deployment will likely use:

```text
S3 static hosting
+ CloudFront CDN
```

instead of long-running frontend containers.

---

## Related Decisions

- 002-use-ecs-fargate.md
- 006-avoid-kubernetes-v1.md
- 010-use-react-vite-frontend.md