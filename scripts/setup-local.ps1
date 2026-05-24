Write-Host "Setting up TranscribeOps local environment..."

if (-Not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example"
} else {
    Write-Host ".env already exists"
}

Write-Host "Local setup complete."