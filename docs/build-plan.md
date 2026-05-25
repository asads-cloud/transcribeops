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