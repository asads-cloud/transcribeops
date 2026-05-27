# SECURITY

# Purpose

This document outlines the current and planned security strategy for TranscribeOps.

The project is intentionally designed to demonstrate production-minded security practices alongside functionality and infrastructure engineering.

Security controls are introduced incrementally throughout the build phases.

---

# Security Principles

The platform prioritises:

- Least privilege access
- Isolation between services
- Input validation
- Abuse prevention
- Cost-protection security
- Secure-by-default infrastructure
- Explicit operational boundaries

---

# Current Local Security Controls

## File Upload Validation

The backend currently validates:

- File extensions
- File size limits
- Multipart upload handling

Accepted file types:

```text
.mp3
.wav
.m4a
```

Invalid file types are rejected with HTTP 400 responses.

---

## Upload Size Limits

Uploads are currently limited to:

```text
5 MB
```

This helps reduce:

- Abuse risk
- Resource exhaustion
- Excessive local compute usage

---

## Isolated Worker Processing

The transcription worker runs independently from the backend API.

Benefits:

- Separation of responsibilities
- Reduced blast radius
- Better future IAM isolation
- Easier operational control

---

## Container Isolation

Services are currently isolated using Docker containers:

```text
frontend
backend
worker
```

This mirrors future cloud service boundaries.

---

## CORS Restrictions

The backend explicitly defines allowed frontend origins during local development.

Example:

```text
http://127.0.0.1:5173
http://localhost:5173
```

This prevents unrestricted browser-based API access.

---

# Planned AWS Security Strategy

## IAM Least Privilege

Future AWS deployment will use least-privilege IAM policies.

Planned separation:

| Service | Permissions |
|---|---|
| Frontend | No AWS credentials |
| Backend API | S3 upload + DynamoDB write + SQS publish |
| Worker | S3 read/write + DynamoDB update + SQS consume |
| Terraform | Infrastructure provisioning only |

---

## Private Worker Networking

Planned ECS worker tasks will run inside private subnets.

Workers will not require direct public internet exposure.

Benefits:

- Reduced attack surface
- Better network isolation
- Easier outbound traffic control

---

## S3 Security Controls

Planned protections include:

- Private buckets only
- Block public access enabled
- Presigned upload URLs
- Prefix isolation
- Lifecycle cleanup policies
- Encryption at rest

---

## Queue Isolation

SQS will isolate:

- Public API traffic
- Internal transcription workloads

Benefits:

- Reduced backend blocking
- Controlled scaling
- Failure isolation
- Safer retry handling

---

## WAF Protection

Future deployment will introduce AWS WAF protections.

Planned controls:

- Rate limiting
- Basic bot protection
- Abuse mitigation
- Request filtering

---

## HTTPS Enforcement

Future production deployment will use:

- ACM certificates
- CloudFront HTTPS
- TLS termination
- Secure browser communication

HTTP-only access will not be permitted in production.

---

## Secrets Management

Secrets will not be hardcoded into containers or repositories.

Future secret management strategy includes:

- Environment variables
- AWS Secrets Manager
- ECS task secrets
- GitHub Actions secret storage

---

# Abuse Prevention

Transcription systems are vulnerable to compute abuse due to expensive audio processing.

The project intentionally includes planned abuse protections:

- File size limits
- Upload validation
- Queue isolation
- Worker scaling controls
- WAF rate limiting
- Short object retention
- IAM isolation

---

# Logging and Monitoring

Future security monitoring will include:

- CloudWatch logging
- ECS task monitoring
- Failed job visibility
- Alarm thresholds
- Queue depth monitoring
- Cost anomaly alerts

---

# Dependency Management

The project uses explicit dependency files:

```text
backend/requirements.txt
worker/requirements.txt
frontend/package.json
```

This improves:

- Reproducibility
- Version visibility
- Dependency auditing

---

# Planned Future Security Enhancements

Potential future improvements include:

- Antivirus scanning
- Audio malware analysis
- Signed upload policies
- Request authentication
- User accounts
- JWT authentication
- API rate limiting
- Audit logging
- Security scanning in CI/CD
- Automated dependency vulnerability checks

---

# Security Limitations (Current Local Phase)

Current local development intentionally prioritises simplicity.

The following are not yet implemented:

- Authentication
- HTTPS
- User isolation
- Production-grade secret management
- WAF protection
- DDoS mitigation
- Advanced monitoring
- Audit trails

These will be introduced during AWS deployment phases.

---

# Operational Philosophy

Security is treated as a core architectural concern rather than a final-stage addition.

The project intentionally demonstrates:

- Incremental hardening
- Infrastructure isolation
- Cost-aware security controls
- Operationally realistic cloud security planning

The architecture prioritises clear service boundaries and predictable operational behaviour over unnecessary complexity.