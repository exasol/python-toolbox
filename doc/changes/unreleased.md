# Unreleased

## Summary

This release fixes vulnerabilities by updating transitive dependencies in the `poetry.lock` file.

| Dependency   | Version | ID             | Fix Versions | Updated to |
|--------------|---------|----------------|--------------|------------|
| cryptography | 46.0.5  | CVE-2026-34073 | 46.0.6       | 46.0.6     |
| pygments     | 2.19.2  | CVE-2026-4539  | 2.20.0       | 2.20.0     |
| requests     | 2.32.5  | CVE-2026-25645 | 2.33.0       | 2.33.1     |

To ensure usage of secure packages, it is up to the user to similarly relock their dependencies.

## Features

* #740: Added nox session `release:update`

## Security Issues

* #759: Fixed vulnerabilities by re-locking transitive dependencies
