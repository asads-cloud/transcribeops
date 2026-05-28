# 015 - Use Terraform for Foundation Infrastructure

## Status

Accepted

## Context

The project requires reproducible AWS infrastructure for development and future deployment environments.

Manual AWS resource creation would:
- reduce reproducibility
- increase configuration drift risk
- weaken recruiter-facing engineering quality
- make CI/CD automation harder later

The system requires:
- S3 buckets
- SQS queues
- DynamoDB tables
- IAM policies

These resources should be declarative and version controlled.

## Decision

Use Terraform as the infrastructure-as-code tool for AWS resource provisioning.

Initial infrastructure includes:
- uploads S3 bucket
- transcripts S3 bucket
- transcription SQS queue
- dead-letter queue
- DynamoDB jobs table
- least-privilege IAM policies

Infrastructure is organised by environment:

```text
infra/environments/dev/
```

Terraform outputs expose resource names and URLs for later application integration phases.

## Consequences

### Positive

- Reproducible infrastructure
- Version-controlled cloud resources
- Easier future CI/CD integration
- Clear recruiter-facing DevOps practices
- Safer infrastructure evolution

### Negative
- Additional tooling complexity
- Terraform state management required
- Future remote backend configuration needed