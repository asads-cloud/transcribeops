Write-Host "Running TranscribeOps tests..."

Write-Host "Building test images..."
docker compose build backend worker

if ($LASTEXITCODE -ne 0) {
    Write-Error "Docker image build failed."
    exit 1
}

Write-Host "Running backend tests..."
docker compose run --rm `
    -v "${PWD}\backend:/app" `
    backend `
    python -m pytest tests

if ($LASTEXITCODE -ne 0) {
    Write-Error "Backend tests failed."
    exit 1
}

$workerTestFiles = Get-ChildItem -Path "worker\tests" -Filter "test_*.py" -Recurse -ErrorAction SilentlyContinue

if ($workerTestFiles) {
    Write-Host "Running worker tests..."
    docker compose run --rm `
        -v "${PWD}\worker:/app" `
        worker `
        python -m pytest tests

    if ($LASTEXITCODE -ne 0) {
        Write-Error "Worker tests failed."
        exit 1
    }
} else {
    Write-Host "No worker test files found. Skipping worker tests."
}

Write-Host "All tests completed successfully."