# 014 - Introduce Service Abstractions

## Status

Accepted

## Context

The application originally coupled backend routes directly to:

- local filesystem storage
- in-memory job storage
- local queue simulation

This would make future AWS integration difficult because infrastructure concerns would be scattered throughout the codebase.

The project requires future support for:

- S3 object storage
- SQS messaging
- DynamoDB persistence

while preserving local development workflows.

## Decision

Introduce service abstraction layers between application logic and infrastructure implementations.

The backend now depends on interfaces instead of concrete implementations.

Service categories introduced:

- StorageService
- QueueService
- JobRepository

Local implementations:

- LocalStorageService
- LocalQueueService
- LocalJobRepository

Future AWS implementations prepared:

- S3StorageService
- SQSQueueService
- DynamoDBJobRepository

Environment variables determine which implementation is loaded.

## Consequences

### Positive

- Cleaner architecture
- Easier AWS migration
- Improved testability
- Reduced infrastructure coupling
- Better long-term maintainability
- Easier local development preservation

### Negative

- Increased initial abstraction complexity
- Additional factory/service boilerplate