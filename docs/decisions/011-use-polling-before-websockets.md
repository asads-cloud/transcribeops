# 011 - Use Polling Before WebSockets

## Status

Accepted

---

## Context

The frontend required a mechanism to monitor asynchronous transcription job progress.

The system needed to display transitions such as:

```text
uploaded
processing
completed
failed
```

Real-time communication options considered included:

- HTTP polling
- WebSockets
- Server-sent events

The project prioritised implementation simplicity and operational clarity during early development phases.

---

## Decision

Use simple interval-based HTTP polling from the frontend to the backend API.

The frontend polls the backend periodically to retrieve updated job status and transcript availability.

Polling occurs every few seconds during active processing.

---

## Consequences

### Positive

- Very simple implementation
- Easy debugging
- No persistent connection management
- Works naturally behind load balancers
- Minimal backend complexity
- Easy ECS and CloudFront compatibility later

### Negative

- Additional repeated HTTP requests
- Slightly higher latency compared to real-time streaming
- Less efficient than event-driven approaches

---

## Alternatives Considered

### WebSockets

Rejected initially because:

- Increased implementation complexity
- Additional operational complexity
- Stateful connection management unnecessary for MVP
- No strong business requirement for real-time streaming

---

### Server-Sent Events

Rejected initially because:

- More complexity than polling
- Limited practical benefit for low-frequency job updates

---

## Operational Impact

Polling keeps the backend stateless and simple during early infrastructure phases.

This simplifies future deployment behind:

- ALB
- ECS/Fargate
- CloudFront

without introducing persistent connection concerns.

---

## Future Reconsideration

Future versions may consider:

- WebSockets
- Server-sent events
- Adaptive polling
- Queue-driven event systems

if scaling or UX requirements justify the additional complexity.

---

## Related Decisions

- 001-use-sqs.md
- 002-use-ecs-fargate.md
- 010-use-react-vite-frontend.md