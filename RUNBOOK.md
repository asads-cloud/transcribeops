# RUNBOOK

## Local Development

### Start Backend

```powershell
uvicorn app.main:app --reload
```

### Run Tests

```powershell
python -m pytest
```

## Local Storage

Uploads are stored under:

```text
local_storage/uploads/
```

Generated transcripts will be stored under:

```text
local_storage/transcripts/
```