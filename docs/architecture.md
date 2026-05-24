# TranscribeOps Architecture

## System Purpose

TranscribeOps is a cloud transcription platform where a user uploads an audio file, the backend creates a transcription job, a worker processes the job asynchronously, and the user later retrieves the completed transcript.

The system is designed around a clear job lifecycle so the API, worker, queue, storage, and database each have well-defined responsibilities.

---

## High-Level Flow

1. User creates a transcription job.
2. Backend creates a job record in DynamoDB.
3. Backend provides an S3 upload location.
4. User uploads audio to S3.
5. User notifies backend that upload is complete.
6. Backend marks the job as queued.
7. Backend sends a message to SQS.
8. Worker receives the SQS message.
9. Worker downloads the audio file from S3.
10. Worker transcribes the audio.
11. Worker uploads transcript to S3.
12. Worker updates the DynamoDB job record.
13. User polls the backend for job status.
14. User retrieves transcript when complete.

---

## Core Components

### Frontend

The frontend is responsible for:

- allowing the user to create a job
- uploading audio using the backend-provided upload flow
- notifying the backend when upload is complete
- polling job status
- displaying the final transcript

The frontend does not directly create queue messages or update job status.

### Backend API

The backend is responsible for:

- creating job records
- validating job IDs
- managing job status transitions before worker processing
- generating S3 upload paths
- sending SQS messages
- reading job metadata from DynamoDB
- returning transcript content to the frontend

The backend owns the API contract.

### Worker

The worker is responsible for:

- consuming transcription jobs from SQS
- downloading uploaded audio from S3
- running Whisper transcription
- uploading transcript output to S3
- updating job status in DynamoDB
- recording processing failures

The worker does not create jobs.

### S3

S3 stores:

- uploaded audio files
- generated transcript files

### SQS

SQS stores transcription work messages.

It decouples the backend from the slower Whisper transcription process.

### DynamoDB

DynamoDB stores job metadata and job state.

It is the source of truth for job status.

---

## Job Lifecycle

Valid job statuses:

| Status | Meaning | Owner |
|---|---|---|
| `created` | Job record exists but upload has not started yet. | Backend |
| `uploading` | Upload process has started or upload details have been issued. | Backend |
| `uploaded` | Audio file has been uploaded to S3. | Backend |
| `queued` | Job has been placed onto SQS for processing. | Backend |
| `processing` | Worker has received the job and started transcription. | Worker |
| `completed` | Worker finished transcription and uploaded the transcript. | Worker |
| `failed` | Job failed during upload, queueing, or processing. | Backend / Worker |
| `expired` | Job was not completed within the allowed lifetime. | Backend / Maintenance process |

Expected normal flow:

```text
created → uploading → uploaded → queued → processing → completed
```

Failure flow:

```text
created/uploading/uploaded/queued/processing → failed
```

Expiry flow:

```text
created/uploading/uploaded/queued → expired
```

### Job Object

A job represents one transcription request.

Example job object:

```json
{
  "job_id": "uuid",
  "status": "created",
  "upload_key": "uploads/job_id/audio.mp3",
  "transcript_key": null,
  "created_at": "timestamp",
  "updated_at": "timestamp",
  "expires_at": "timestamp",
  "error_message": null,
  "file_size_bytes": 0,
  "model": "tiny"
}
```

## Field Definitions

| Field | Type | Description |
|---|---|---|
| `job_id` | `string` | Unique job identifier, generated as a UUID. |
| `status` | `string` | Current job lifecycle status. |
| `upload_key` | `string` | S3 object key for the uploaded audio file. |
| `transcript_key` | `string \| null` | S3 object key for the transcript file after completion. |
| `created_at` | `string` | Timestamp when the job was created. |
| `updated_at` | `string` | Timestamp when the job was last updated. |
| `expires_at` | `string` | Timestamp after which the job should be considered expired. |
| `error_message` | `string \| null` | Failure reason if the job fails. |
| `file_size_bytes` | `number` | Uploaded audio file size in bytes. |
| `model` | `string` | Whisper model used for transcription. Default: `tiny`. |

### S3 Object Paths

Uploaded audio files:

```text
uploads/{job_id}/audio.mp3
```

Transcript files:

```text
transcripts/{job_id}/transcript.txt
```

Example:

```text
uploads/123e4567-e89b-12d3-a456-426614174000/audio.mp3
transcripts/123e4567-e89b-12d3-a456-426614174000/transcript.txt
```

S3 should not be used as the source of truth for job state. DynamoDB owns state.

### SQS Message Format

The backend sends this message after upload completion:

```json
{
  "job_id": "uuid",
  "upload_bucket": "bucket-name",
  "upload_key": "uploads/job_id/audio.mp3",
  "transcript_bucket": "bucket-name",
  "transcript_key": "transcripts/job_id/transcript.txt",
  "model": "tiny"
}
```

## Field Definitions

| Field | Type | Description |
|---|---|---|
| `job_id` | `string` | Job identifier matching DynamoDB. |
| `upload_bucket` | `string` | S3 bucket containing uploaded audio. |
| `upload_key` | `string` | S3 key for uploaded audio. |
| `transcript_bucket` | `string` | S3 bucket where transcript will be written. |
| `transcript_key` | `string` | S3 key where transcript will be saved. |
| `model` | `string` | Whisper model selected for processing. |

SQS messages should contain only the information needed by the worker to process the job.

### DynamoDB Item Shape

DynamoDB stores one item per transcription job.

Primary key:

```text
PK: job_id
```

Example item:

```json
{
  "job_id": "uuid",
  "status": "created",
  "upload_key": "uploads/job_id/audio.mp3",
  "transcript_key": null,
  "created_at": "timestamp",
  "updated_at": "timestamp",
  "expires_at": "timestamp",
  "error_message": null,
  "file_size_bytes": 0,
  "model": "tiny"
}
```

DynamoDB is used for:

- creating jobs
- tracking status
- storing object keys
- recording failures
- checking expiry
- returning job metadata to the frontend

## API Contract

### `GET /health`

Checks whether the backend service is running.

#### Response

```json
{
  "status": "ok"
}
```
### `POST /jobs`

Creates a new transcription job.

#### Backend Responsibilities

- generate `job_id`
- create upload S3 key
- create transcript S3 key
- create DynamoDB job item
- return job metadata to the frontend

#### Example Response

```json
{
  "job_id": "uuid",
  "status": "created",
  "upload_key": "uploads/job_id/audio.mp3",
  "transcript_key": null,
  "model": "tiny"
}
```
### `POST /jobs/{job_id}/complete-upload`

Marks an upload as complete and queues the job for processing.

#### Backend Responsibilities

- validate that the job exists
- update status to `uploaded`
- send SQS message
- update status to `queued`

#### Example Response

```json
{
  "job_id": "uuid",
  "status": "queued"
}
```

### `GET /jobs/{job_id}`

Returns current job metadata.

#### Example Response

```json
{
  "job_id": "uuid",
  "status": "processing",
  "upload_key": "uploads/job_id/audio.mp3",
  "transcript_key": null,
  "created_at": "timestamp",
  "updated_at": "timestamp",
  "expires_at": "timestamp",
  "error_message": null,
  "file_size_bytes": 123456,
  "model": "tiny"
}
```

### `GET /jobs/{job_id}/transcript`

Returns transcript content for a completed job.

#### If the Job Is Complete

```json
{
  "job_id": "uuid",
  "transcript": "Example transcript text."
}
```

If the job is not complete:

```json
{
  "error": "Transcript is not available yet."
}
```

## Ownership Boundaries

### Backend Owns

- API endpoints
- job creation
- upload completion
- SQS publishing
- pre-processing status changes
- reading job status
- serving transcript content

---

### Worker Owns

- SQS consumption
- transcription processing
- transcript upload
- processing status updates
- processing failure handling

---

### S3 Owns

- audio object storage
- transcript object storage

---

### SQS Owns

- asynchronous work delivery
- retry handling
- dead-letter queue handoff later

---

### DynamoDB Owns

- job metadata
- job status
- object key references
- expiry metadata
- error metadata