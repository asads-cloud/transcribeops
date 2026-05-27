Write-Host "Cleaning TranscribeOps local environment..."

Write-Host "Stopping and removing Docker Compose containers..."
docker compose down --remove-orphans

if ($LASTEXITCODE -ne 0) {
    Write-Error "Docker Compose cleanup failed."
    exit 1
}

Write-Host "Removing local uploaded files..."
Remove-Item -Recurse -Force "local_storage\uploads" -ErrorAction SilentlyContinue

Write-Host "Removing local transcript files..."
Remove-Item -Recurse -Force "local_storage\transcripts" -ErrorAction SilentlyContinue

Write-Host "Recreating local storage folders..."
New-Item -ItemType Directory -Force -Path "local_storage\uploads" | Out-Null
New-Item -ItemType Directory -Force -Path "local_storage\transcripts" | Out-Null

Write-Host "Local environment cleaned successfully."