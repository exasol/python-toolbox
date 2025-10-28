# Unreleased

## Feature

* #494: Created check of built packages with nox session `package:check`

## Refactoring

* #578: Updated GitHub actions which now use node 24:
   * actions/checkout to [v5](https://github.com/actions/checkout/releases/tag/v5.0.0)
   * actions/download-artifact to [v6](https://github.com/actions/download-artifact/releases/tag/v6.0.0)
   * actions/upload-artifact to [v5](https://github.com/actions/upload-artifact/releases/tag/v5.0.0)

## Security

* #578: Resolved CVE-2024-12797 for cryptography and CVE-2025-8869 for pip by updating the lock file
