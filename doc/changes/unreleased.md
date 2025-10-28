# Unreleased

## Feature

* #494: Created check of built packages with nox session `package:check`

## Refactoring

* #578: Updated actions/checkout to [v5](https://github.com/actions/checkout/releases/tag/v5.0.0), which uses node 24

## Security

* #578: Resolved CVE-2024-12797 for cryptography and CVE-2025-8869 for pip by updating the lock file
