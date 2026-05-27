# 010 - Use React + Vite Frontend

## Status

Accepted

---

## Context

The platform required a recruiter-facing frontend that could:

- Upload audio files
- Display job status
- Poll asynchronous transcription progress
- Render completed transcripts
- Explain system architecture visually

The frontend needed to remain lightweight while supporting future integration with AWS-hosted backend infrastructure.

The project also required rapid local iteration during development.

---

## Decision

Use:

- React for frontend application development
- Vite for frontend tooling and local development server

The frontend is implemented as a standalone application communicating with the FastAPI backend through HTTP APIs.

---

## Consequences

### Positive

- Fast local development iteration
- Minimal frontend boilerplate
- Clear component structure
- Strong ecosystem and recruiter familiarity
- Easy Docker integration
- Easy future deployment to S3 + CloudFront
- Clean separation between frontend and backend concerns

### Negative

- Additional frontend build tooling introduced
- Separate dependency management required
- Browser-based CORS handling required

---

## Alternatives Considered

### Plain HTML Templates

Rejected because:

- Harder to evolve into production-style frontend
- Poor recruiter signalling
- Reduced frontend architecture separation

---

### Next.js

Rejected initially because:

- SSR complexity unnecessary for MVP
- Additional deployment complexity
- Larger framework surface area than required

May be reconsidered later if SSR or advanced frontend routing becomes valuable.

---

## Operational Impact

The frontend now runs independently from the backend and worker services.

This more accurately reflects future production deployment patterns using:

```text
CloudFront
→ Frontend
→ Backend API
→ Worker Services
```

---

## Related Decisions

- 002-use-ecs-fargate.md
- 006-avoid-kubernetes-v1.md