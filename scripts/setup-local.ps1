Write-Host "Setting up TranscribeOps local environment..."

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker is not installed or not available in PATH."
    exit 1
}

if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "Created .env from .env.example"
    } else {
        Write-Error ".env.example not found."
        exit 1
    }
} else {
    Write-Host ".env already exists"
}

New-Item -ItemType Directory -Force -Path "local_storage\uploads" | Out-Null
New-Item -ItemType Directory -Force -Path "local_storage\transcripts" | Out-Null

Write-Host "Starting local app with Docker Compose..."

docker compose up --build