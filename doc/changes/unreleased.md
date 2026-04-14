# Unreleased

## Summary

This release includes an update of `action/upload-pages-artifact` from v4 to v5.0.0. With this
change, now all actions used in the PTB run with Node.js 24. This is important as support
for Node.js 20 reaches it end-of-life in April 2026 and support for it in GitHub will end in
September 2026; for more details, see GitHub's [deprecation notice](https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/).

The `report.yml` is also called after the `checks.yml` completes. This allows users
to get linting, security, and unit test coverage before running the `slow-checks.yml`,
as described in the [Pull Request description](https://exasol.github.io/python-toolbox/main/user_guide/features/github_workflows/index.html#pull-request).

This release also adds a `vulnerabilities:resolved` Nox session, which reports GitHub security issues resolved since the last release.

This release fixes a vulnerability by updating the `poetry.lock` file.

| Name   | Version | ID             | Fix Versions | Updated to |
|--------|---------|----------------|--------------|------------|
| pytest | 9.0.2   | CVE-2025-71176 | 9.0.3        | 9.0.3      |

To ensure usage of secure packages, it is up to the user to similarly relock their dependencies.

## Features

* #402: Created nox session `vulnerabilities:resolved` to report resolved GitHub security issues
* #733: Adjusted structlog and log level for workflow generation

## Refactoring

* #764: Updated `action/upload-pages-artifact` from v4 to [v5](https://github.com/actions/upload-pages-artifact/releases/tag/v5.0.0)
* #768: Updated `merge-gate.yml` to execute the `report.yml` after the `checks.yml` completes

## Bugfix

* #766: Fixed `action/upload-pages-artifact` from v5 to v5.0.0

## Security

* #774: Fixed vulnerability by re-locking `pytest` in the `poetry.lock`
