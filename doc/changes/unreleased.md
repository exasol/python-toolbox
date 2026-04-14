# Unreleased

## Summary

This release includes an update of `action/upload-pages-artifact` from v4 to v5.0.0. With this
change, now all actions used in the PTB run with Node.js 24. This is important as support
for Node.js 20 reaches it end-of-life in April 2026 and support for it in GitHub will end in
September 2026; for more details, see GitHub's [deprecation notice](https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/).

The `report.yml` is also called after the `checks.yml` completes. This allows users
to get linting, security, and unit test coverage before running the `slow-checks.yml`,
as described in the [Pull Request description](https://exasol.github.io/python-toolbox/main/user_guide/features/github_workflows/index.html#pull-request).

## Refactoring

* #764: Updated `action/upload-pages-artifact` from v4 to [v5](https://github.com/actions/upload-pages-artifact/releases/tag/v5.0.0)
* #768: Updated `merge-gate.yml` to execute the `report.yml` after the `checks.yml` completes

## Bugfix

* #766: Fixed `action/upload-pages-artifact` from v5 to v5.0.0

## Feature

* #733: Adjusted structlog and log level for workflow generation
