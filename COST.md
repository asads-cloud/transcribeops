# COST

# Purpose

This document defines the cost-management strategy for TranscribeOps.

The platform is intentionally designed to demonstrate production-minded cloud engineering with explicit focus on:

- Cost visibility
- Abuse prevention
- Resource isolation
- Budget enforcement
- Predictable scaling behaviour

The project prioritises operational discipline alongside functionality.

---

# Local Development Costs

## Current Local Runtime

Current development runs entirely locally using:

- Docker Desktop
- FastAPI
- React/Vite
- Whisper
- Local filesystem storage

No active AWS infrastructure costs currently exist.

---

# Planned AWS Cost Strategy

The production-style AWS deployment is intentionally designed to minimise unnecessary cloud spend while preserving realistic architecture patterns.

---

# Core Cost-Control Principles

## 1. Scale Only When Needed

The system uses asynchronous processing so compute resources activate only when jobs exist.

Examples:

- ECS tasks scale independently
- Workers process queue-based workloads
- Frontend remains statically hosted

---

## 2. Separate Cheap Storage From Expensive Compute

Storage and compute are intentionally separated.

| Resource | Purpose |
|---|---|
| S3 | Cheap durable object storage |
| ECS/Fargate | Short-lived compute workloads |
| DynamoDB | Lightweight metadata storage |
| SQS | Low-cost asynchronous buffering |

---

## 3. Minimise Always-On Infrastructure

The architecture intentionally avoids unnecessarily expensive always-running systems.

Examples:

- No Kubernetes cluster
- No EC2 management overhead
- No GPU infrastructure initially
- No large persistent databases

---

# Planned AWS Services and Cost Controls

## S3

### Planned Protections

- Lifecycle policies for automatic cleanup
- Object expiration policies
- Separate upload and transcript prefixes
- No public bucket access
- Storage class optimisation later if required

### Abuse Prevention

- File size upload limits
- Audio-type validation
- Presigned upload URLs
- Short object retention windows

---

## ECS/Fargate

### Planned Protections

- Small task sizes initially
- Worker autoscaling limits
- CPU-only inference initially
- Environment isolation between dev and prod

### Future Optimisations

Potential future improvements:

- Spot capacity
- GPU worker separation
- Queue-driven autoscaling
- Scale-to-zero patterns

---

## SQS

### Planned Protections

- Dead-letter queue (DLQ)
- Visibility timeout tuning
- Retry limits
- Queue depth monitoring

SQS selected specifically because it is low-cost and operationally simple.

---

## DynamoDB

### Planned Protections

- On-demand billing initially
- TTL-based item expiration
- Simple access patterns
- Minimal indexed attributes

DynamoDB selected specifically because the workload does not require relational complexity.

---

## CloudWatch

### Planned Protections

- Log retention limits
- Alarm thresholds
- Minimal high-volume debug logging in production
- Service-level monitoring only where valuable

---

## CloudFront

### Planned Protections

- CDN caching for static frontend assets
- Reduced backend traffic
- HTTPS termination at edge

---

## WAF

### Planned Protections

- Rate limiting
- Basic abuse prevention
- Upload request protection
- Bot mitigation later if required

---

# Planned Budgeting Controls

## AWS Budgets

Planned monthly budgets:

| Environment | Budget |
|---|---|
| Dev | Low fixed cap |
| Prod Demo | Controlled showcase budget |

Budget alerts will notify on:

- Forecasted overspend
- Actual overspend
- Sudden traffic spikes

---

# Abuse Prevention Strategy

Transcription systems are vulnerable to abuse because audio processing is compute-intensive.

The platform intentionally includes planned protections:

- File size limits
- Audio validation
- Rate limiting
- Queue isolation
- Worker scaling limits
- WAF protections
- Private worker networking
- Least-privilege IAM policies

---

# Architectural Cost Decisions

## Why ECS/Fargate Instead of Kubernetes

Kubernetes introduces unnecessary operational and infrastructure overhead for this project size.

ECS/Fargate provides:

- Lower operational complexity
- Lower idle costs
- Faster deployment
- Simpler networking
- Simpler IAM integration

---

## Why DynamoDB Instead of RDS

The workload only requires:

- Create job
- Update job status
- Retrieve job by ID

Relational joins are unnecessary.

DynamoDB significantly reduces:

- Operational overhead
- Scaling complexity
- Infrastructure cost

---

## Why SQS Instead of Direct Processing

SQS allows:

- Worker decoupling
- Controlled scaling
- Failure isolation
- Reduced backend blocking
- More predictable compute utilisation

This lowers operational risk and compute waste.

---

# Planned Future Optimisations

Potential future enhancements include:

- GPU inference workers
- Spot compute capacity
- Adaptive autoscaling
- Multi-queue prioritisation
- Intelligent transcript retention policies
- Audio compression workflows
- Cached transcript delivery

---

# Current Constraints

## CPU-only Whisper

Current local development uses CPU-only inference.

Longer files process more slowly but reduce local hardware requirements.

---

## Local Storage

Current local runtime uses bind-mounted Docker storage:

```text
./local_storage
```

This will later migrate to:

```text
S3 object storage
```

---

# Operational Philosophy

TranscribeOps is intentionally designed to demonstrate:

- Responsible cloud engineering
- Cost-aware architecture design
- Production-minded operational thinking
- Abuse-resistant infrastructure planning

The project prioritises simplicity, operational clarity, and predictable scaling behaviour over unnecessary architectural complexity.