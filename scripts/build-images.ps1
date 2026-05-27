Write-Host "Building TranscribeOps Docker images..."

Write-Host "Building backend image..."
docker compose build backend

Write-Host "Building worker image..."
docker compose build worker

Write-Host "Building frontend image..."
docker compose build frontend

Write-Host "All Docker images built successfully."