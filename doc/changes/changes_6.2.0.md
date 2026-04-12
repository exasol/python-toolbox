# 6.2.0 - 2026-04-10

## Summary

This release fixes vulnerabilities by updating transitive dependencies in the `poetry.lock` file.

| Dependency   | Version | ID             | Fix Versions | Updated to |
|--------------|---------|----------------|--------------|------------|
| cryptography | 46.0.5  | CVE-2026-34073 | 46.0.6       | 46.0.7     |
| cryptography | 46.0.6  | CVE-2026-39892 | 46.0.7       | 46.0.7     |
| pygments     | 2.19.2  | CVE-2026-4539  | 2.20.0       | 2.20.0     |
| requests     | 2.32.5  | CVE-2026-25645 | 2.33.0       | 2.33.1     |

To ensure usage of secure packages, it is up to the user to similarly relock their dependencies.

## Features

* #740: Added nox session `release:update`

## Security Issues

* #759: Fixed vulnerabilities by re-locking transitive dependencies & updated `actions/deploy-pages` from v4 to v5

## Dependency Updates

### `main`

* Updated dependency `pysonar:1.3.0.4086` to `1.0.2.1722`
