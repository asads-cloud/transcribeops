# 013 - Use PowerShell for Local Automation

## Status

Accepted

---

## Context

TranscribeOps is primarily developed on Windows using:

- PowerShell
- Docker Desktop
- VS Code
- AWS CLI
- Terraform

Running Docker commands manually creates friction during development and increases onboarding complexity.

The project requires repeatable local workflows for:

- environment setup
- image builds
- automated testing
- cleanup/reset operations
- container orchestration

The project also aims to demonstrate platform engineering and automation skills alongside cloud infrastructure engineering.

---

## Decision

Use PowerShell scripts to automate local development workflows.

The following scripts are introduced:

```text
scripts/setup-local.ps1
scripts/run-tests.ps1
scripts/build-images.ps1
scripts/clean-local.ps1
```

The scripts automate:

- Docker validation
- `.env` bootstrapping
- local storage setup
- Docker Compose startup
- image builds
- automated test execution
- local cleanup workflows

---

## Consequences

### Positive

- Faster local onboarding
- Reduced manual setup errors
- More consistent local workflows
- Improved developer experience
- Better operational reproducibility
- Demonstrates automation and scripting ability
- Creates a foundation for future deployment automation

### Negative

- Scripts are currently Windows-focused
- Additional maintenance overhead for automation scripts
- Linux/macOS equivalents may eventually be required

---

## Alternatives Considered

### Manual Docker Commands

Rejected because:

- repetitive
- error-prone
- poor onboarding experience
- weaker operational maturity

### Makefiles

Rejected because the primary development environment is Windows.

PowerShell provides a more natural Windows-native workflow.

### Bash Scripts

Rejected because the project intentionally prioritises Windows tooling and PowerShell automation skills.

---

## Future Considerations

Potential future improvements include:

- environment validation scripts
- AWS validation scripts
- deployment automation
- log tailing utilities
- Terraform orchestration helpers
- CI/CD workflow integration

The current scripts intentionally focus only on local developer workflows.
